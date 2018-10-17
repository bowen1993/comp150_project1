# Comp 150 Working with Corpora Project 1 Group 1

## Data Preparation

Run the following command to generate file in JSON format

```
python preData.py
```

Generate text files for all characters

```
python segText2Files.py
```

### Directory Structure

All text data files are under directory data

```
data/
    Christopher_Marlowe/
        marl.jew.json
        marl.massacre.json
        marl.jew/
        	all txt files for each character (role_id.txt)
        marl.massacre
          all txt files for each character (role_id.txt)
    Globe_Shakespeare/
        all json files for each play... (1h4.json ...)
    	1h4\
            all txt files for each character (role_id.txt)
    	1h6\
    	2h4\
    	2h6\
		3h6\
		ado\
		ant\
		aww\
		ayl\
		cor\
```