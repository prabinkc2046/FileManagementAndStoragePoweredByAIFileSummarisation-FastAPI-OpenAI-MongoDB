# Standard library imports if any

# Third party imports
from fastapi import File, UploadFile, FastAPI, HTTPException, Query, Depends, status

# module required for /token 
from user import get_current_active_user

# import module required for /extract 
from extraction.validate_filetype import validate_filetype
from extraction.check_filetype_and_extract import check_filetype_and_extract

# module required for /summarise
from open_ai.request_summary import summarise_text
from secret.retrieve_secret import retrieve_secret

async def get_summary(  
    words: int, #number of words to be extracted from file
    max_tokens: int, # total units of words that open ai will process including input and output
    summary_counts: int, # number of words for summary of the extracted text
    # secret_info:dict,
    file: UploadFile = File(...),
    current_active_user: dict = Depends(get_current_active_user),
):
    # check the validity of the file type
    # throws error if the filetype is not pdf or doc or docx
    validate_filetype(file)

    # extract the text from the matching file type
    # default input words count is 100 unless stated as /summarise?words=200
    text = await check_filetype_and_extract(file, words)
    
    # If text is empty, raise and error
    if not text:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message":"text could not be extracted from the file"}
        )
    
    # Get open api key
    # OPENAI_API_KEY = secret_info.get("open_api_key")

    # Validate open api key
    # if OPENAI_API_KEY is None:
    #     raise HTTPException(
    #     status_code=status.HTTP_400_BAD_REQUEST,
    #     detail={"message": "Open api key is not provided. Please provide open api key"}
    # )
    
    # Validate max tokens
    if max_tokens <= 0:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"message": "max_tokens must be greater than 0"}
    )

    # Validate words count
    if words <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "The number of words must be greater than 0"}
        )

    # Validate summary words count
    if summary_counts <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "summary_counts must be greater than 0"}
        )

    # summary = await summarise_text(
    #         openai_api_key=OPENAI_API_KEY,
    #         text=text,
    #         max_tokens=max_tokens,
    #         summary_words_count=summary_counts
    #     )
    
    # If summary is empty, raise and error
    # if not summary:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail={"message":"summary could not be created"}
    #     )

    summary = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam ea delectus esse sapiente commodi, et mollitia aut! Dignissimos, vero consectetur! Quia voluptatibus provident minus, ipsa at culpa sint, fugit, velit laboriosam non eligendi molestias repellat itaque quo quam obcaecati recusandae! Labore, magni dolorem molestias esse officiis, consequuntur consectetur maiores nemo cumque magnam inventore in soluta distinctio? Mollitia sed cumque itaque velit est dolor adipisci amet, harum quibusdam eius fugit libero veniam aliquam voluptate. A magnam vero autem iste natus! Exercitationem temporibus, veniam eum est enim eos fugit officiis, eaque dolorem animi ducimus at quisquam, id maxime perferendis odit commodi cupiditate quas magni nostrum illum doloremque doloribus dignissimos aut. Dolorum ad sed provident consectetur eaque distinctio dolorem magni labore dolor excepturi, sapiente commodi harum. Provident et perspiciatis magnam corporis dolorem animi temporibus molestiae cum facilis. Corrupti accusamus distinctio obcaecati provident sapiente magnam nobis molestias molestiae, facere repellat voluptates pariatur non quae ducimus, at amet eum, odit unde labore corporis. Ipsum obcaecati sit iusto quibusdam incidunt aliquid ducimus reiciendis veritatis non vel, a hic et voluptate reprehenderit tempore quas itaque odit iure accusamus sunt laborum, quidem quis error. Recusandae optio provident illo sapiente numquam, labore, aliquam blanditiis laborum at nobis natus soluta magnam harum. Reiciendis magni alias exercitationem quibusdam sapiente natus quis suscipit ullam mollitia at enim cupiditate incidunt voluptatibus neque, quidem saepe! Iure praesentium nam totam provident consequuntur? Eaque ipsa, in aspernatur architecto rerum nulla repellat dolor quis numquam ab qui ut veniam hic! Maiores quo animi maxime pariatur quasi ratione, ducimus repellat, temporibus, rem nam nostrum. Veritatis eaque repudiandae quasi consequatur explicabo. Est nostrum, et eos saepe corrupti dignissimos, reprehenderit quasi ad sit perferendis beatae. Eaque repellat recusandae earum deleniti quod fugiat voluptatum voluptates deserunt? Eligendi, et animi repellat officia quisquam reprehenderit aut dicta sit nostrum, eum possimus. Quas exercitationem at dolorem repellat, aperiam perspiciatis impedit, pariatur dolorum porro consequatur dolor! Ducimus nulla officiis nesciunt. Quisquam ipsa sit at, quidem itaque voluptates obcaecati suscipit ipsum voluptatibus repudiandae maiores quae dolorem nostrum illo minima nobis deserunt velit rem assumenda exercitationem dolores molestias? Suscipit, a impedit ipsa doloribus iure dignissimos ipsam vel reiciendis eum vitae, aliquam, repellendus ex labore at? Fugit numquam doloribus laudantium reiciendis ex. Mollitia saepe aspernatur provident molestias magni officiis at delectus magnam, sunt expedita. Repudiandae corporis et culpa exercitationem, enim ipsa molestias saepe aperiam ut veritatis ab consequatur modi, similique natus? Explicabo sed maiores itaque vitae accusantium, dolor accusamus aspernatur magnam id repellendus est incidunt nostrum voluptate, maxime vel! Numquam deserunt assumenda, dolorum dignissimos pariatur, amet mollitia perspiciatis aliquid asperiores non fuga nobis dicta. Suscipit non, aliquid amet deleniti delectus animi et, fugiat quia quis tenetur nobis explicabo voluptatibus, doloremque aliquam ut? Aliquid libero distinctio, voluptate suscipit amet iusto a cupiditate enim eius veritatis perspiciatis? Soluta eligendi inventore nobis laboriosam exercitationem qui cupiditate voluptatem aperiam alias libero architecto tenetur quisquam nemo explicabo iste consequuntur voluptate, deserunt accusamus unde veritatis et! Adipisci in magnam eum sit numquam id odio ipsum quidem, repellendus facilis, laborum dolorum exercitationem nulla, expedita earum reiciendis! Dolores molestias, quis placeat sed sapiente in voluptas alias expedita cupiditate atque similique vitae dolore repudiandae illo officiis, temporibus quod corrupti. Culpa, dolorem quae consequatur optio itaque commodi expedita nobis accusamus! Quibusdam ipsum tempore, corrupti fuga nesciunt nobis blanditiis maxime asperiores officia minus! Asperiores dignissimos at temporibus sapiente, maiores tempore. Iste, vitae, eaque ab neque animi at veniam eius deserunt incidunt nam vero tempora inventore. Ad excepturi alias vitae veniam iste, dolore temporibus nam placeat fugiat ipsum porro magni eius repellat. Esse sit facere qui, atque amet soluta quisquam perspiciatis sint aut quia iste natus eaque possimus illum eligendi consequuntur accusamus explicabo id laborum modi repellat cum unde. Beatae quos neque magni a natus odio laboriosam earum nesciunt laudantium, expedita est mollitia inventore incidunt id dolor eos quia ab amet ratione fugiat? Nobis ratione animi corrupti! Quibusdam facere fuga eveniet aspernatur libero veritatis eius animi minus amet neque nihil ullam fugit tempore similique molestias in, deleniti at laudantium! Eligendi laborum ipsum amet dicta aperiam quis. Rem tenetur et rerum tempora quod, asperiores quae error distinctio, nisi voluptatem sequi non numquam repellendus explicabo qui. Quidem ratione quasi velit delectus dolor adipisci fugiat recusandae quis omnis ipsa. Nihil nobis sequi dolores facere velit eos vel dicta quas enim officiis, non consequatur maiores! Dolore voluptas libero consequatur aliquam sunt officia delectus blanditiis corporis nostrum eligendi at, odit numquam dolorum iusto labore. Quasi quia quisquam illo voluptate modi a ducimus neque facere libero, fuga cum eveniet aliquam id. Similique architecto porro voluptate ipsum dolore autem, aperiam quasi? Cum voluptas, possimus et alias quasi repellendus necessitatibus fugiat dolorem omnis numquam aliquid ipsa mollitia doloremque iste. Perspiciatis incidunt inventore totam eaque, soluta debitis illum deserunt porro, delectus, animi facere architecto earum aspernatur cumque? Ipsa in alias asperiores natus aut quam quas unde iusto nemo modi veritatis, quos reiciendis mollitia eum soluta accusantium sit quaerat vitae. Accusamus ipsa eligendi facilis deserunt aspernatur doloremque, exercitationem voluptas voluptates animi id quia, ipsum sunt. Esse placeat illo quis nobis, commodi soluta eum pariatur, similique error ab quisquam voluptatibus aliquid? Neque ullam laborum fugit eum, libero, iure magnam, atque officiis ad impedit modi delectus ducimus mollitia adipisci commodi. Corrupti vero consequuntur, delectus atque cum maxime nihil! Sapiente impedit sint aliquid libero totam accusamus minima, culpa ullam modi explicabo nulla possimus aut ut molestias suscipit porro cum commodi! Fuga quibusdam debitis reiciendis officia harum eaque dolorem alias nam? Ratione voluptatum doloremque assumenda, iste voluptatibus dignissimos, quia eos incidunt deleniti quas itaque officia cupiditate nobis repellat laborum labore! Optio quam sunt neque similique in maiores perferendis animi tempore dolor accusamus voluptatem fugiat corrupti nulla, eaque deleniti necessitatibus illo fugit. Et, placeat! Cupiditate, optio aut! Maxime corrupti ipsam ipsa nulla iste culpa, distinctio ratione voluptatibus eos quis. Perspiciatis eos porro facilis et voluptatibus voluptates, commodi aperiam rerum adipisci non voluptate reprehenderit, deleniti quam recusandae suscipit ipsum, excepturi odio dolores quo! Odio quos commodi dicta doloribus delectus ullam quas recusandae ab atque possimus, optio labore voluptates fugiat? Error magni, vitae pariatur accusamus dolorem dolores!"
    return {"summary": summary}
