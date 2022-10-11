This is an API for annotating audio data (any url has to go in the static/ directory).
Plans for features include:
- open dataset from csv file
- find the right audio file to pair with dataset (maybe also with context?)
- annotation options for each row of the dataset
- each cell should be editable

Todo:
1. Save:
    a. in 'app.py', add POST page (figure out how)
    b. in 'annotation_page', add save button config
2. Submit:
    a. hit submit, loading page show up (optional)
    b. on the server:
        i. save temp data as json file
        ii. save data as .csv file
        iii. pop up telling you the directory that it saved, as to hit "see analysis"
3. See Analysis (diff html):
        i. use results to generate graphs, diff text
        ii. panel for revising results?