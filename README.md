<!-- Project Header -->
## Gemini Analyze csv file with Streamlit

### Overview
Create gemini app can using csv file e.g. app can analyze data from csv file etc.

![Run Result](result/Run_Gemini_API_Result.gif)

### Usage
Follow these steps to set up and run the project:

1. Create .env file under root folder then add following variable

```sh
GEMINI_API_KE0=[Your API Key]
```

2. Install dependencies

```sh
pip install google-generativeai
pip install streamlit
```

3. Update streamlit to be the latest version

```sh
pip install --upgrade streamlit
```

4. Run the Streamlit server

```sh
streamlit run app_chat.py
```

5. Access the application in your browser at http://localhost:8501.

### Repository Structure

```sh
repository/
├── app_chat.py          # the code and UI integrated together live here
├── data/                # keep original cvs data
├── img/                 # keep image files 
├── result/              # keep the example result after run.

```
