# nim-sum
Silly app trying to play some nim

TODO make installable and put on AWS. For now...

To use, first clone repo. Then cd into `nim-sum` folder. 

Assume person has Flask installed. Need to add some environment variables. Type:
`export FLASK_APP=nimsum`
and 
`export FLASK_ENV=development`

Next run `flask init-db`. 

Now `flask run` should run the app. Click the URL that is spit out and hit "new game" to play. 

NOTES:
Don't enter number of piles before hitting new game, there is a routing bug.
When playing, the player and computers moves are processed both at once. Better display of moves to come. 
Try not to press refresh on the `play/move` URL. This can repeat a `POST` command and mess with stuff.
