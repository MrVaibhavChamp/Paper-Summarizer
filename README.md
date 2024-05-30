# Paper-Summarizer
<p>This system asks for a domain name, finds ten recent papers related to the domain, creates a vector database, gives a summary, and lets users interact with the documents using gpt-3.5 turbo.</p>



## Running the tool  

Different ways to run the app:


### Run with Docker  

1. Create `.env` file in the root directory of the project, copy and paste the below config, and replace the `{OPENAI_API_KEY}` configuration value with your key.

```bash

OPENAI_API_TOKEN={OPENAI_API_KEY}

HOST=0.0.0.0

PORT=8080

EMBEDDER_LOCATOR=text-embedding-ada-002

EMBEDDING_DIMENSION=1536

MODEL_LOCATOR=gpt-3.5-turbo

MAX_TOKENS=200

TEMPERATURE=0.0

```

2. From the project root folder, open your terminal and run `docker compose up`.

3. Navigate to `localhost:8502` on your browser when docker installation is successful.



### Run from source  

##### Prerequisites

1. [Python](https://www.python.org/downloads/) 3.10 or above

2. Install [Pip](https://pip.pypa.io/en/stable/installation/)

3. [OpenAI](https://openai.com/) account and an API Key([OpenAI](https://openai.com/product))

Now, follow the following steps.

##### Step 1: Clone this repository and navigate to the project folder directory  

```bash

git clone https://github.com/MrVaibhavChamp/Paper-Summarizer.git
cd  Paper-Summarizer

```  

##### Step 2: Set environment variables

Create a `.env` file in the root project directory as described above.


##### Step 3 (Optional): Creating new virtual environment

Create a new virtual environment in the same folder and activate that environment:

```bash

python  -m  venv  pw-env && source  pw-env/bin/activate

```  

#### Step 4: Install the dependencies

Install required packages:

```bash

pip  install  --upgrade  -r  requirements.txt

```  

#### Step 5: Run Pathway API  

You start the application by running `main.py`:


```bash

python  main.py

```
  

#### Step 6: Run Streamlit UI

Run the UI separately by running Streamlit app

`streamlit run ui.py` command. It connects to the Pathway's backend API automatically, and the UI frontend will run on your browser.


### Run with Conda with a Linux-VM/WSL (windows) or linux/macOS terminal (linux/macOS)

1. Clone the repository on your system.

2. Create a `.env` file as discussed already.

3. From the project root folder, open your terminal and run `WSL` if you will be using it.
 
4. Create a conda environment.

5. Activate the conda environment.

6. Install the app dependencies.

Install the required packages:

```bash

pip  install  --upgrade  -r  requirements.txt

```

7. Run the Pathway API.

Start the application by running `main.py`:

```bash

python  main.py

```

8. Run Streamlit UI

You can run the UI separately by running the `streamlit run ui.py` command. It connects to Pathway's API automatically and the UI frontend will be running on your browser.

------------------------------------
### Collaborators: Vaibhav Chaudhary, Argha Kamal Samanta
