# Install

- Install python packages with: `python3 -m pip install numpy vosk`
- Get the ML speech recognition model here: `wget "https://alphacephei.com/vosk/models/"` and unzip in `Models/`. Make sure to update the model name to the one you selected in the python file. At time of writing, there are three models for English: `0.15` (small model), `0.22`, and `0.22-lgraph`. All three seem to work fine.
- Install `ffpeg`: This should not be a requirement but I haven't figured out a way around it yet.

