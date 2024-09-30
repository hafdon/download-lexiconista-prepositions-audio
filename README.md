# MP3 Downloader for Prepositional Forms

This Python script automates the process of constructing URLs for downloadable MP3s and downloading them locally. It works with webpages containing multiple prepositional word forms, extracting the corresponding dialects and downloading the audio files in different dialects (Connacht, Munster, Ulster) for each form.

## Features

- **URL Construction**: Automatically generates the correct URLs for MP3 downloads based on word forms and dialects.
- **MP3 Downloads**: Downloads MP3 files into organized directories (`C`, `M`, `U`) for each dialect.
- **Error Handling**: Includes basic error handling for HTTP requests.

## Prerequisites

- Python 3.x
- Install the required Python libraries:
  ```bash
  pip install requests beautifulsoup4
  ```

## Usage

1. **Add URLs**: Update the `urls` list in the script with the target webpage URLs.
2. **Run the Script**:

   ```bash
   python download_mp3s.py
   ```

3. **Output**: MP3 files will be downloaded into `C`, `M`, and `U` directories for each dialect, named in the format `{preposition}_{word}.mp3`.

## Directory Structure

```
C/
   faoi_fúm.mp3
   faoi_fút.mp3
M/
   faoi_fúm.mp3
   faoi_fút.mp3
U/
   faoi_fúm.mp3
   faoi_fút.mp3
```

## Notes

- Ensure the provided URLs follow the expected structure for proper parsing.
- Logs will display download progress and any errors encountered during execution.
