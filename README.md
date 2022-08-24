# CheckMate

_This system intends to combat misinformation through a simple and accessible system that can validate the credibility of a claim_

Flask API - TO process claims from frontend and return response

Whatsapp Bot - Python script to interact with Twilio and Flask API server. Sends the claim from whatsapp to flask and displays the claim rating.

Discord Bot - Discord bot API interacts with Flask API server. Sends the claim from Discord to flask and displays the claim rating

Similarity Check - Compares 2 sentences by extracting their compute sentence / text embedding and uses cosine_similarity to compare the 2 sentences.

Bert_model - Contains training logs for BERT, along with tokenizer and config files. Note that the model file was not added due to file size limitation


