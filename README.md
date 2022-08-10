# UCI-Browser
## A light browser written in PyQt5

### How to install
| Dependency | Version | Download / Install |
| --- | --- | --- |
| Python | >= 3.8 | [Python.org](https://www.python.org/downloads/) |
| PyQt | `5.15.7`/`5.15.2` | `pip install PyQt5` |
| PyQtWebEngine | Latest | `pip install PyQtWebEngine` |
| requests | Latest | `pip install requests` |

In CMD / Terminal:
```
git clone https://github.com/CuteBladeYT/UCI-Browser
cd UCI-Browser
./browser.py
```

### Settings
Settings are stored in a JSON file.<br>
Here's an example:
```json
{
    "homepage": "https://www.google.com",

    "search_engine": {
        "current": "google",

        "google": "https://www.google.com/search?q=",
        "duckduckgo": "https://www.duckduckgo.com/?q=",
        "bing": "https://www.bing.com/search?q="
    },

    "startup": {
        "maximized": false,
        "size": [800, 600]
    },

    "misc": {
        "max_page_title_length": 30
    }
}

```
The key names pretty much explains themselves.
