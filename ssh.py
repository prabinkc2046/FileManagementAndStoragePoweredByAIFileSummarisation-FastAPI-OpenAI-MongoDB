# Import built in module
import paramiko as pk
from scp import SCPClient
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec, ed25519
from typing import Union
from fastapi import HTTPException
from datetime import datetime
import os


from caching import get_secret_info
from fastapi import Depends


"""Identify the type of the key"""
def identify_key_type(ssh_key_path, pass_phrase: Union[str, None]):
    try:
        with open(ssh_key_path, "rb") as key_file:
            key_data = key_file.read()

        private_key = serialization.load_ssh_private_key(data=key_data, password=pass_phrase.encode() if pass_phrase else None)

        if isinstance(private_key, rsa.RSAPrivateKey):
            return "RSA"
        
        if isinstance(private_key, ec.EllipticCurvePrivateKey):
            return "ECDSA"
        
        if isinstance(private_key, ed25519.Ed25519PrivateKey):
            return "ED25519"
        
        else:
            return "Unknown or unsupported key type"
    
    except ValueError as e:
        return f"Failed to load key: {str(e)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"



"""Load private key from the file path
Also use password key if it is provided, otherwise optional"""
def load_private_key(key_type: str, SSH_KEY_PATH, SSH_PASSWORD_KEY):
    try:
        if SSH_PASSWORD_KEY:
            if key_type == "RSA":
                    pkey = pk.RSAKey.from_private_key_file(SSH_KEY_PATH, password=SSH_PASSWORD_KEY)

            elif key_type == "ECDSA":
                pkey = pk.ECDSAKey.from_private_key_file(SSH_KEY_PATH, password=SSH_PASSWORD_KEY)
            
            elif key_type == "ED25519":
                pkey = pk.Ed25519Key.from_private_key_file(SSH_KEY_PATH, password=SSH_PASSWORD_KEY)
            else:
                raise HTTPException(
                    status_code=500,
                    detail="Unsupported key type. Only RSA, ECDSA and ED25519 types are supported"
                )
        else:
            if key_type == "RSA":
                    pkey = pk.RSAKey.from_private_key_file(SSH_KEY_PATH)

            elif key_type == "ECDSA":
                pkey = pk.ECDSAKey.from_private_key_file(SSH_KEY_PATH)
            
            elif key_type == "ED25519":
                pkey = pk.Ed25519Key.from_private_key_file(SSH_KEY_PATH)
            else:
                raise HTTPException(
                    status_code=500,
                    detail="Unsupported key type. Only RSA, ECDSA and ED25519 types are supported"
                )

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Private key file not found at {SSH_KEY_PATH}"
        )
    except pk.PasswordRequiredException:
        raise HTTPException(
            status_code=500,
            detail="Private key is encrypted, and no password was provided"
        )
    except pk.SSHException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load private key:{str(e)}"
        )
    return pkey


"""Create SSH client"""
def create_ssh_client(private_key, hostname, username):
    try:
        # Initialise SSH client
        ssh_client = pk.SSHClient()
        ssh_client.set_missing_host_key_policy(pk.AutoAddPolicy())
        
        # Connect to the remote server
        ssh_client.connect(
            hostname=hostname, 
            username=username, 
            pkey=private_key,
            timeout=30
        )
        
        # use SCP to send the file
        return ssh_client
    
    except pk.AuthenticationException:
        raise HTTPException(
            status_code=401,
            detail="Authentication failed: Incorrect username or private key"
        )
    except pk.SSHException as e:
        raise HTTPException(
            status_code=500,
            detail=f"SSH error occurred: {str(e)}"
        )
    except pk.BadHostKeyException:
        raise HTTPException(
            status_code=500,
            detail="Server's host key could not be verified"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )


# Creats an SSH client and SCP client
async def create_scp_client(remote_host, remote_user, password=None, pkey=None):
    
    # Initialise SSH client
    ssh = pk.SSHClient()
    ssh.set_missing_host_key_policy(pk.AutoAddPolicy())
    ssh.connect(
        hostname=remote_host,
        username=remote_user,
        password=password,
        pkey=pkey
    )

    # Create SCP client
    scp = SCPClient(ssh.get_transport())
    return scp, ssh


"""Copy file from temporary file path to the remote server"""
# save file to the remote server
def save_file_to_remote_server(temp_file_path, remote_storage_directory, ssh_client):
    try:

        # Create an SCP client using the SSH client
        with SCPClient(ssh_client.get_transport()) as scp:
            # Send the file
            scp.put(temp_file_path, remote_path=remote_storage_directory)
        
        # Close connection
        ssh_client.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send file: {str(e)}")

# Download file from the remote server
def get_file_from_remote(remote_path, ssh_client, scp_client, local_temp_dir="/tmp"):
    try:
        local_file_path = os.path.join(local_temp_dir, os.path.basename(remote_path))
        print("the filename from the remote server is", os.path.basename(remote_path))
        scp_client.get(remote_path, local_file_path)
        ssh_client.close()
        scp_client.close()
        return local_file_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download file: {str(e)}")
       


