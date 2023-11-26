# gpt4-turbo
GPT4 Turbo local memory conversational chat is an experiment. It helps those how don't have access to the GPT4-turbo on the Open AI ChatGPT console.

# Language Chain Chatbot

This Python script utilizes the LangChain library to create a chatbot with conversational memory. The chatbot uses OpenAI's GPT-4 language model to generate responses based on user input.

## Installation

Make sure you have [Python](https://www.python.org/) and [pipenv](https://pypi.org/project/pipenv/) installed on your system.

1. Clone this repository:

    ```bash
    git clone https://github.com/levinskipolish/gpt4-turbo.git
    ```

2. Navigate to the project directory:

    ```bash
    cd /gpt4-turbo
    ```

3. Install dependencies using pipenv:

    ```bash
    pipenv install
    ```
4. Environment variables(You mus have an [OPENAI](https://openai.com/product) account and an API KEY):
    ```bash
    cp .env-example .env && echo 'OPENAI_API_KEY="<Your OPENAI API KEY Here"' >> .env
    ```
5. Activate the virtual environment:

    ```bash
    pipenv shell
    ```

## Usage

Run the following command to start the chatbot:

```bash
python3 chat.py
```
## Example
```
You: How far electrons are orbiting the nucleus of an atom if the nucleus was the size of an apple?
```
```
AI: Visualizing atomic structures on a scale we can relate to is a great way to grasp the vast differences in size within the universe. If we were to scale up an atom so that its nucleus was the size of an apple, we would have to deal with a huge increase in scale, as atoms are incredibly small.

The nucleus of an atom is roughly 10^-15 meters in diameter, while the entire atom's diameter, including its electron cloud, is about 10^-10 meters. This means that if we scale up the nucleus to the size of an apple, approximately 10 centimeters in diameter, we're increasing its size by a factor of 10^14 (100 picometers/1 femtometer = 10^14).

Using this scale, if the nucleus (the apple) is at the center of a large space, the electrons would be orbiting at a distance comparable to the size of a large sports stadium or even beyond. This is because electrons do not have fixed orbits but rather exist in probability clouds known as orbitals, which can extend quite far from the nucleus.

So, if the nucleus were the size of an apple, the electrons would be found in a cloud with a radius of several kilometers, emphasizing just how much of an atom is empty space. This analogy helps illustrate the scale but remember that actual atoms and their behavior are governed by the principles of quantum mechanics, which are much more complex than simple planetary orbits.
```
```
You: exit
```
```
AI: Okay, if you wish to end our interaction, feel free to close this chat window. There's no formal command needed to exit. If you have more questions in the future or simply want to talk, don't hesitate to return. Have a great day!
```