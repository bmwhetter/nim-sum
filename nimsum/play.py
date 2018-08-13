import functools
import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from nimsum.db import get_db
from nimsum.nim import NimPiles

bp = Blueprint('play', __name__, url_prefix='/play')

@bp.route('/move', methods=('GET', 'POST'))
def move():
    # Get current position from the database
    db = get_db()
    game_id = session.get('game_id')
    g.position_string = db.execute(
        'SELECT piles FROM positions WHERE game_id = ? ORDER BY id DESC', 
        (game_id,)
    ).fetchone()['piles']
    if request.method == 'POST':    
        error = None
        pile = int(request.form['pile'])
        stones = int(request.form['stones'])
        n = NimPiles(g.position_string)
        
        if error is not None:
            flash(error)

        else:
            # process player move
            n.remove_stones(pile, stones)
            piles_string = n.stringify_piles()
            db.execute(
                'INSERT INTO positions (game_id, piles) VALUES (?, ?)', 
                (game_id, piles_string)
            )
            db.commit()

            if n.game_over():
                return redirect(url_for('play.win'))

            # If the nim sum is already 0 computer plays random, else optimal
            if n.nim_sum_zero():
                pile, stones = n.gen_random_move() 
            else:
                pile, stones = n.gen_optimal_move()

            n.remove_stones(pile, stones)
            piles_string = n.stringify_piles()
            db.execute(
                'INSERT INTO positions (game_id, piles) VALUES (?, ?)', 
                (game_id, piles_string)
            )
            db.commit()
            if n.game_over():
                return redirect(url_for('play.lose'))
            
            return redirect(url_for('play.move'))    

    return render_template('play/move.html')

@bp.route('/win', methods=('GET',))
def win():
    return render_template('play/win.html')

@bp.route('/lose', methods=('GET',))
def lose():
    return render_template('play/lose.html')