import functools
import uuid
import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from nimsum.db import get_db

bp = Blueprint('newgame', __name__, url_prefix='/newgame')

@bp.route('/piles', methods=('GET', 'POST'))
def piles():
    # clear session before doing anything else
    session.clear()
    if request.method == 'POST':
        num_piles = int(request.form['num_piles'])
        db = get_db()
        error = None

        if not num_piles:
            error = 'Please enter a number of piles!'
        
        if error is None:
            game_id = str(uuid.uuid4())
            db.execute(
                'INSERT INTO games (id, num_piles) VALUES (?, ?)', 
                (game_id, num_piles)
            )

            db.commit()
            session['game_id'] = game_id
            session['num_piles'] = num_piles
            session['pile_names'] = ['pile {}'.format(i) for i in range(1, num_piles+1, 1)]
            return redirect(url_for('newgame.stones'))

        flash(error)

    return render_template('newgame/piles.html')

@bp.route('/stones', methods=('GET', 'POST'))
def stones():
    if request.method == 'POST':
        pile_dict = {}
        for pile in session.get('pile_names'):
            pile_dict[pile] = int(request.form[pile])

        pile_string = json.dumps(pile_dict)
        db = get_db()
        error = None

        if error is None:
            db.execute(
                'INSERT INTO positions (game_id, piles) VALUES (?, ?)',
                (session.get('game_id'), pile_string)
            )
            db.commit()
            return redirect(url_for('play.move'))

        flash(error)

    return render_template('newgame/stones.html')

@bp.before_app_request
def load_current_game():
    game_id = session.get('game_id')

    if game_id is None:
        g.game_id = None
    else:
        g.game = get_db().execute(
            'SELECT * FROM games WHERE id = ?', (game_id,)
        ).fetchone()
