import openai

# return the summarised text from open ai
async def summarise_text(openai_api_key, text, max_tokens=100, summary_words_count=50):
    """Make an api request to get the summarised text from extracted text input"""
    # default max_tokens is 100
    # default summary word count is 50
    openai.api_key = openai_api_key
    
    # Define the prompt for summarisation
    prompt = f"Summarise the following text in {summary_words_count} words:\n{text}"

    # Make the API request for summary
    response = openai.chat.completions.create(
        max_tokens=max_tokens,
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract summary from the response
    summary = response.choices[0].message.content

    # return summary
    return summary


