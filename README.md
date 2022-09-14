# Python CLI for running a web search

```bash
# Install Requirements

pip install -r requirements.txt

# Help

./search.py
./search.py --help

# Use default engine
search.py search "terraform templates" 

# Other engines
./search.py search "terraform templates" --engine=startpage
./search.py search "terraform templates" --engine=bing
./search.py search york --engine=gmaps

# Search for paste buffer contents
./search.py search

# List available engines
./search.py engines
```
