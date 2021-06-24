import sys
import time
import numpy as np
import pygame as pg


pg.init()
screen = pg.display.set_mode((1000, 600))
pg.display.set_caption('ChessEngine')
clock = pg.time.Clock()
coor_font = pg.font.SysFont('Arial', size=15)
result_font = pg.font.SysFont('Arial', size=30, bold=True)
mode_font = pg.font.SysFont('Arial', size=24, bold=True)

path = 'C:\\Users\\Robert\\Documents\\chess_pics\\'
back_ground = pg.image.load(path + 'back-ground.png').convert()
chess_board = pg.image.load(path + 'chess-board.png').convert()
chess_board_rect = chess_board.get_rect(topleft=(44, 44))
option_board = pg.image.load(path + 'option-board.png').convert()
game_mode = pg.image.load(path + 'game-mode.png').convert()
first_option, second_option = pg.Rect(674, 144, 253, 56), pg.Rect(674, 211, 253, 56)
top_option = pg.Rect(674, 120, 253, 49)
middle_option = pg.Rect(674, 179, 253, 49)
bottom_option = pg.Rect(674, 238, 253, 49)
dark_square = pg.image.load(path + 'dark-square.png').convert_alpha()
promo_strip = pg.image.load(path + 'promo-strip.png').convert()
w_pawn = pg.image.load(path + 'w-pawn.png').convert_alpha()
b_pawn = pg.image.load(path + 'b-pawn.png').convert_alpha()
w_rook = pg.image.load(path + 'w-rook.png').convert_alpha()
b_rook = pg.image.load(path + 'b-rook.png').convert_alpha()
w_bishop = pg.image.load(path + 'w-bishop.png').convert_alpha()
b_bishop = pg.image.load(path + 'b-bishop.png').convert_alpha()
w_night = pg.image.load(path + 'w-night.png').convert_alpha()
b_night = pg.image.load(path + 'b-night.png').convert_alpha()
w_queen = pg.image.load(path + 'w-queen.png').convert_alpha()
b_queen = pg.image.load(path + 'b-queen.png').convert_alpha()
w_king = pg.image.load(path + 'w-king.png').convert_alpha()
b_king = pg.image.load(path + 'b-king.png').convert_alpha()


class ChessPiece:
    def __init__(self, col, name):
        self.col = col
        self.name = name

    def pos(self, x=None):
        return positions[self.name] if x is None else positions[self.name][x]

    def __str__(self):
        raise NotImplementedError

    def legal_move(self, x=0):
        raise NotImplementedError

    def import_func(self):
        def move_gen(pos1, pos2, rnge=range(1, 2)):
            att_sq, legalmoves = [], []
            for n in rnge:
                a = np.array(self.pos()) + np.array([n * pos1, n * pos2])
                if (a[0] not in range(8)) or (a[1] not in range(8)):
                    break
                b, c = list(positions.values()).index(a.tolist()), pawns
                if np.sign(Board[c[b].pos(0), c[b].pos(1)]) == np.sign(self.col):
                    att_sq.append(a.tolist())
                    break
                legalmoves.append(a.tolist())
                att_sq.append(a.tolist())
                if np.sign(Board[c[b].pos(0), c[b].pos(1)]) == np.sign(-self.col):
                    break
            return att_sq, legalmoves
        return move_gen


class Pawn(ChessPiece):
    def __str__(self):
        return 'pawns'

    def legal_move(self, x=0):
        legalmoves, att_sq = [], []
        a = np.array(self.pos()) - askr * self.col * np.array([1, 0])
        b = np.array(self.pos()) - askr * self.col * np.array([2, 0])
        if self.pos(0) not in [0, 7]:
            if (-askr * self.col == 1 and self.pos(1) != 0) or (-askr * self.col == -1 and self.pos(1) != 7):
                c = np.array(self.pos()) - askr * self.col * np.array([1, -1])
                if np.sign(Board[list(c)[0], list(c)[1]]) == np.sign(-1 * self.col):
                    legalmoves.append(c.tolist())
                    att_sq.append(c.tolist())
                elif np.sign(Board[list(c)[0], list(c)[1]]) != np.sign(-1 * self.col):
                    att_sq.append(c.tolist())
            if (-askr * self.col == 1 and self.pos(1) != 7) or (-askr * self.col == -1 and self.pos(1) != 0):
                d = np.array(self.pos()) - askr * self.col * np.array([1, 1])
                if np.sign(Board[list(d)[0], list(d)[1]]) == np.sign(-1 * self.col):
                    legalmoves.append(d.tolist())
                    att_sq.append(d.tolist())
                elif np.sign(Board[list(d)[0], list(d)[1]]) != np.sign(-1 * self.col):
                    att_sq.append(d.tolist())
        cond1a = game_moves[-1][1] == list(np.array(self.pos()) - askr * self.col * np.array([0, 1]))
        cond1b = game_moves[-1][1] == list(np.array(self.pos()) - askr * self.col * np.array([0, -1]))
        cond2 = game_moves[-1][0] == list(np.array(game_moves[-1][1]) - askr * self.col * np.array([2, 0]))
        cond3 = abs(pawns[list(positions.values()).index(game_moves[-1][1])].col) == 1
        if (cond1a or cond1b) and cond2 and cond3:
            side = np.array([1, 1]) if cond1a else np.array([1, -1])
            e = np.array(self.pos()) - askr * self.col * side
            legalmoves.append(e.tolist())
        start = 1 if -askr * self.col == 1 else 6
        if self.pos(0) not in [0, 7]:
            if start == self.pos(0) and not Board[list(a)[0], list(a)[1]] and not Board[list(b)[0], list(b)[1]]:
                legalmoves.append(b.tolist())
                legalmoves.append(a.tolist())
            elif not Board[list(a)[0], list(a)[1]]:
                legalmoves.append(a.tolist())
            else:
                pass
        if not legalmoves:
            legalmoves.append([])
        if not att_sq:
            att_sq.append([])
        return legalmoves if x == 0 else att_sq


class Rook(ChessPiece):
    def __str__(self):
        return 'rooks'

    def legal_move(self, x=0):
        move_gen = ChessPiece.import_func(self)
        rlegalmoves, ratt_sq = [], []
        ranges = [range(1, 1+self.pos(0)), range(1, 8-self.pos(0)), range(1, 1+self.pos(1)), range(1, 8-self.pos(1))]
        for asq, lm in map(move_gen, [-1, 1, 0, 0], [0, 0, -1, 1], ranges):
            rlegalmoves.extend(lm)
            ratt_sq.extend(asq)
        if not rlegalmoves:
            rlegalmoves.append([])
        if not ratt_sq:
            ratt_sq.append([])
        return rlegalmoves if x == 0 else ratt_sq


class Bishop(ChessPiece):
    def __str__(self):
        return 'bishops'

    def legal_move(self, x=0):
        move_gen = ChessPiece.import_func(self)
        blegalmoves, batt_sq = [], []
        ranges = [range(1, 8 - self.pos(1)) if 8 - self.pos(0) > 8 - self.pos(1) else range(1, 8 - self.pos(0)),
                  range(1, 1 + self.pos(1)) if self.pos(0) + self.pos(1) <= 7 else range(1, 8 - self.pos(0)),
                  range(1, 1 + self.pos(0)) if self.pos(0) + self.pos(1) <= 7 else range(1, 8 - self.pos(1)),
                  range(1, 1 + self.pos(0)) if self.pos(0) < self.pos(1) else range(1, 1 + self.pos(1))]
        for asq, lm in map(move_gen, [1, 1, -1, -1], [1, -1, 1, -1], ranges):
            blegalmoves.extend(lm)
            batt_sq.extend(asq)
        if not blegalmoves:
            blegalmoves.append([])
        if not batt_sq:
            batt_sq.append([])
        return blegalmoves if x == 0 else batt_sq


class Queen(ChessPiece):
    def __str__(self):
        return 'queens'

    def legal_move(self, x=0):
        move_gen = ChessPiece.import_func(self)
        qlegalmoves, qatt_sq = [], []
        ranges = [range(1, 1+self.pos(0)), range(1, 8-self.pos(0)), range(1, 1+self.pos(1)), range(1, 8-self.pos(1)),
                  range(1, 8 - self.pos(1)) if 8 - self.pos(0) > 8 - self.pos(1) else range(1, 8 - self.pos(0)),
                  range(1, 1 + self.pos(1)) if self.pos(0) + self.pos(1) <= 7 else range(1, 8 - self.pos(0)),
                  range(1, 1 + self.pos(0)) if self.pos(0) + self.pos(1) <= 7 else range(1, 8 - self.pos(1)),
                  range(1, 1 + self.pos(0)) if self.pos(0) < self.pos(1) else range(1, 1 + self.pos(1))]
        for asq, lm in map(move_gen, [-1, 1, 0, 0, 1, 1, -1, -1], [0, 0, -1, 1, 1, -1, 1, -1], ranges):
            qlegalmoves.extend(lm)
            qatt_sq.extend(asq)
        if not qlegalmoves:
            qlegalmoves.append([])
        if not qatt_sq:
            qatt_sq.append([])
        return qlegalmoves if x == 0 else qatt_sq


class Night(ChessPiece):
    def __str__(self):
        return 'nights'

    def legal_move(self, x=0):
        move_gen = ChessPiece.import_func(self)
        nlegalmoves, natt_sq = [], []
        for asq, lm in map(move_gen, [2, 2, -2, -2, 1, -1, 1, -1], [1, -1, 1, -1, 2, 2, -2, -2]):
            nlegalmoves.extend(lm)
            natt_sq.extend(asq)
        if not nlegalmoves:
            nlegalmoves.append([])
        if not natt_sq:
            natt_sq.append([])
        return nlegalmoves if x == 0 else natt_sq


class King(ChessPiece):
    def __str__(self):
        return 'kings'

    def legal_move(self, x=0):
        move_gen = ChessPiece.import_func(self)
        klegalmoves, katt_sq = [], []
        for asq, lm in map(move_gen, [1, 1, -1, -1, -1, 1, 0, 0], [1, -1, 1, -1, 0, 0, -1, 1]):
            klegalmoves.extend(lm)
            katt_sq.extend(asq)
        whch = np.sign(self.col) == askr
        whch1 = np.sign(self.col) == -askr
        rdat = [0, 7] if player1 == 'White' else [7, 0]
        arook = np.sign(rooks[rdat[0]].col) == askr
        hrook = np.sign(rooks[rdat[1]].col) == askr
        rdat1 = [56, 63] if player1 == 'White' else [63, 56]
        arook1 = np.sign(rooks[rdat1[0]].col) == -askr
        hrook1 = np.sign(rooks[rdat1[1]].col) == -askr
        if x == 0:
            if (not kingm and not arm and whch and arook) or (not kingm1 and not arm1 and whch1 and arook1):
                if not check(np.sign(self.col)):
                    ap = list(np.array(self.pos()) + askr * np.array([0, 1]))
                    bp = list(np.array(self.pos()) + askr * np.array([0, 2]))
                    if (ap[1] not in range(8)) or (bp[1] not in range(8)):
                        return
                    apos = list(positions.values()).index(ap)
                    bpos = list(positions.values()).index(bp)
                    if Board[kings[apos].pos(0), kings[apos].pos(1)] == 0 and Board[
                       kings[bpos].pos(0), kings[bpos].pos(1)] == 0 and not check(np.sign(self.col), x=ap):
                        lmm = move_gen(0, askr * 2)
                        klegalmoves.extend(lmm[1])
            if (not kingm and not hrm and whch and hrook) or (not kingm1 and not hrm1 and whch1 and hrook1):
                if not check(np.sign(self.col)):
                    ap = list(np.array(self.pos()) + askr * np.array([0, -1]))
                    bp = list(np.array(self.pos()) + askr * np.array([0, -2]))
                    if (ap[1] not in range(8)) or (bp[1] not in range(8)):
                        return
                    apos = list(positions.values()).index(ap)
                    bpos = list(positions.values()).index(bp)
                    if Board[kings[apos].pos(0), kings[apos].pos(1)] == 0 and Board[
                       kings[bpos].pos(0), kings[bpos].pos(1)] == 0 and not check(np.sign(self.col), x=ap):
                        lmm = move_gen(0, askr * -2)
                        klegalmoves.extend(lmm[1])
        if not klegalmoves:
            klegalmoves.append([])
        if not katt_sq:
            katt_sq.append([])
        return klegalmoves if x == 0 else katt_sq


def start_piece(config='standard'):
    if config == 'standard':
        qpos, kpos = [[3, 59], [4, 60]] if askr == -1 else [[4, 60], [3, 59]]
        for i, pki in enumerate(list(positions.keys())):
            pawns[i], rooks[i], bishops[i] = Pawn(0, pki), Rook(0, pki), Bishop(0, pki)
            nights[i], queens[i], kings[i] = Night(0, pki), Queen(0, pki), King(0, pki)
            if (i in range(8, 16)) or (i in range(48, 56)):
                pawns[i].col = askr if i in range(8, 16) else -askr
            if i in [0, 7, 56, 63]:
                rooks[i].col = 5 * askr if i in [0, 7] else -5 * askr
            if i in [2, 5, 58, 61]:
                bishops[i].col = 4 * askr if i in [2, 5] else -4 * askr
            if i in [1, 6, 57, 62]:
                nights[i].col = 3 * askr if i in [1, 6] else -3 * askr
            if i in qpos:
                queens[i].col = 9 * askr if i == qpos[0] else -9 * askr
            if i in kpos:
                kings[i].col = 10 * askr if i == kpos[0] else -10 * askr


def update_board():
    for u in range(64):
        a, b, c, d, e, f = pieces
        if a[u].col == 0 and b[u].col == 0 and c[u].col == 0 and d[u].col == 0 and e[u].col == 0 and f[u].col == 0:
            Board[a[u].pos(0), a[u].pos(1)] = 0
        elif a[u].col != 0:
            Board[a[u].pos(0), a[u].pos(1)] = a[u].col
        elif b[u].col != 0:
            Board[b[u].pos(0), b[u].pos(1)] = b[u].col
        elif c[u].col != 0:
            Board[c[u].pos(0), c[u].pos(1)] = c[u].col
        elif d[u].col != 0:
            Board[d[u].pos(0), d[u].pos(1)] = d[u].col
        elif e[u].col != 0:
            Board[e[u].pos(0), e[u].pos(1)] = e[u].col
        elif f[u].col != 0:
            Board[f[u].pos(0), f[u].pos(1)] = f[u].col
    return Board


def check(cols, x=None):
    update_board()
    kingpos, pk = [], set([])
    for pce in pieces:
        for q in range(64):
            if np.sign(pce[q].col) == -cols:
                [pk.add(tuple(x)) for x in pce[q].legal_move(1)]
    for t in range(64):
        if kings[t].col == 10 * cols:
            kingpos = tuple(kings[t].pos())
    return kingpos in pk if x is None else tuple(x) in pk


def newpiecepos(pce, mve, px, copy=False, redo=False, ra1=0, rb1=0, rc1=None):
    a1, b1, c1 = [], [], []
    pce_cop = pieces.copy()
    mind = list(positions.values()).index(mve)
    pce_cop.remove(kings)
    if pce == kings:
        pass
    else:
        pce_cop.remove(pce)
    if copy and not redo:
        a1 = pce[mind].col
        b1 = pce[px].col
        c1 = [str(x[0])[0] for x in pce_cop]
        for pcoc in pce_cop:
            c1[c1.index(str(pcoc[0])[0])] = pcoc[mind].col
    if not redo:
        pce[mind].col = pce[px].col
        pce[px].col = 0
        for pcoc in pce_cop:
            pcoc[mind].col = 0
    if copy and not redo:
        return a1, b1, c1
    if redo:
        c2 = [str(x[0])[0] for x in pce_cop]
        pce[mind].col = ra1
        pce[px].col = rb1
        for pcoc in pce_cop:
            pcoc[mind].col = rc1[c2.index(str(pcoc[0])[0])]


def list_move(cols):
    legalm, legald = [], []
    for pce in pieces:
        pcel, pcein, pname = [], [], []
        pcelm, pname0, pname1 = [], [], []
        for q in range(64):
            if np.sign(pce[q].col) == cols:
                pcel.append(pce[q].legal_move())
                pcein.append(q)
                pname.append(pce[q].name)
        [pcelm.append(f) for g in pcel for f in g]
        [pname0.append(g[0]) for g in pname]
        [pname1.append(g[1]) for g in pname]
        for u, x1 in enumerate(pcein):
            for x2 in pcel[u]:
                enps, castle = False, False
                an, cast, qn = '', '', ''
                x0 = pce[x1].pos()
                co = pce[x1].name
                if not x2:
                    continue
                ci = list(positions.values()).index(x2)
                cn = pce[ci].name
                bn = 'x' if Board[x2[0], x2[1]] != 0 else ''
                if pce == pawns and Board[x2[0], x2[1]] == 0 and x0[1] != x2[1]:
                    enps, bn = True, 'x'
                    sx = 1 if player1 == 'White' else -1
                    pawns[ci + sx * cols * 8].col = 0
                if pce == kings and ((x0[1] + 2 == x2[1]) or (x0[1] - 2 == x2[1])):
                    castle, newrook, oldrook = True, [], []
                    if cols == askr:
                        newrook = [3, 5] if player1 == 'White' else [2, 4]
                        oldrook = [0, 7]
                    elif cols == -askr:
                        newrook = [59, 61] if player1 == 'White' else [58, 60]
                        oldrook = [56, 63]
                    if x0[1] + 2 == x2[1]:
                        rooks[oldrook[1]].col = 0
                        rooks[newrook[1]].col = 5 * cols
                        cast = 'O-O' if player1 == 'White' else 'O-O-O'
                    elif x0[1] - 2 == x2[1]:
                        rooks[oldrook[0]].col = 0
                        rooks[newrook[0]].col = 5 * cols
                        cast = 'O-O-O' if player1 == 'White' else 'O-O'
                cd1, ce1, cf1 = newpiecepos(pce, x2, x1, copy=True)
                update_board()
                if not check(cols):
                    legald.append([pce, x2, x1])
                    posin, pecin = [pname0, pname1, pname], [co[0], co[1], co]
                    if pcelm.count(x2) > 1:
                        for x, y in enumerate(pecin):
                            if posin[x].count(y) == 1:
                                an = y
                                break
                    if pce == pawns:
                        pn = ''
                        an = co[0] if bn == 'x' else ''
                        if cn[1] in ['1', '8']:
                            qn = '='
                    else:
                        pn = str(pce[0])[0].upper()
                    if not castle:
                        legalm.append(pn + an + bn + cn + qn)
                    else:
                        legalm.append(cast)
                newpiecepos(pce, x2, x1, redo=True, ra1=cd1, rb1=ce1, rc1=cf1)
                update_board()
                if enps:
                    sx = 1 if player1 == 'White' else -1
                    pawns[ci + sx * cols * 8].col = -cols
                if castle:
                    newrook, oldrook = [], []
                    if cols == askr:
                        newrook = [3, 5] if player1 == 'White' else [2, 4]
                        oldrook = [0, 7]
                    elif cols == -askr:
                        newrook = [59, 61] if player1 == 'White' else [58, 60]
                        oldrook = [56, 63]
                    if x0[1] + 2 == x2[1]:
                        rooks[oldrook[1]].col = 5 * cols
                        rooks[newrook[1]].col = 0
                    elif x0[1] - 2 == x2[1]:
                        rooks[oldrook[0]].col = 5 * cols
                        rooks[newrook[0]].col = 0
    return legalm, legald


def mouse_in_rect(rect):
    x_coord, y_coord = pg.mouse.get_pos()
    return (rect.left <= x_coord <= rect.right) and (rect.top <= y_coord <= rect.bottom)


def coor_display(side):
    locations = list(range(76, 525, 64))
    for il, letter in enumerate(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'][::-side]):
        letter_surface = coor_font.render(letter, True, (255, 187, 130))
        letter_rect = letter_surface.get_rect(center=(locations[il], 566))
        screen.blit(letter_surface, letter_rect)
    for il, number in enumerate(list(range(1, 9))[::side]):
        number_surface = coor_font.render(str(number), True, (255, 187, 130))
        number_rect = number_surface.get_rect(center=(33, locations[il]))
        screen.blit(number_surface, number_rect)


def options_display(note='start'):
    game_choice, bin_choice = '', ''
    ltext, rtext = ['White', 'Black'] if note == 'start' else ['Play again', 'Quit']
    fmode, faskr, fp1, fp2, fc = '', '', '', '', ''
    condition = True
    while condition:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if (event.type == pg.MOUSEBUTTONDOWN) and (event.button == 1):
                if (not game_choice) and (note == 'start'):
                    if mouse_in_rect(top_option):
                        game_choice = 'top'
                    elif mouse_in_rect(middle_option):
                        game_choice = 'mid'
                    elif mouse_in_rect(bottom_option):
                        game_choice = 'bottom'
                else:
                    if note == 'start':
                        if mouse_in_rect(first_option):
                            bin_choice = 'white'
                        elif mouse_in_rect(second_option):
                            bin_choice = 'black'
                    else:
                        if mouse_in_rect(first_option):
                            bin_choice = 'continue'
                        elif mouse_in_rect(second_option):
                            bin_choice = 'quit'

        screen.blit(back_ground, (0, 0))
        screen.blit(chess_board, chess_board_rect)
        if (not game_choice) and (note == 'start'):
            screen.blit(game_mode, (600, 104))
            top_text = mode_font.render('Player Vs. Player', True, (255, 187, 130))
            middle_text = mode_font.render('Player Vs. Computer', True, (255, 187, 130))
            bottom_text = mode_font.render('Computer Vs. Computer', True, (255, 187, 130))
            top_rect = top_text.get_rect(center=(799, 144))
            middle_rect = middle_text.get_rect(center=(799, 204))
            bottom_rect = bottom_text.get_rect(center=(799, 264))
            screen.blit(top_text, top_rect)
            screen.blit(middle_text, middle_rect)
            screen.blit(bottom_text, bottom_rect)
        else:
            if note != 'start':
                for piece in all_pieces:
                    p_type, p_rect = piece
                    screen.blit(p_type, p_rect)
                coor_display(askr)
            screen.blit(option_board, (600, 104))
            left_text = mode_font.render(ltext, True, (255, 187, 130))
            right_text = mode_font.render(rtext, True, (255, 187, 130))
            left_rect = left_text.get_rect(center=(799, 172))
            right_rect = right_text.get_rect(center=(799, 238))
            screen.blit(left_text, left_rect)
            screen.blit(right_text, right_rect)
            if note != 'start':
                result = result_font.render(note, True, (255, 187, 130))
                result_rect = result.get_rect(center=(799, 50))
                screen.blit(result, result_rect)
        condition = (not game_choice) or (not bin_choice) if note == 'start' else (not bin_choice)
        pg.display.update()
        clock.tick(120)
    if note == 'start':
        if game_choice == 'top':
            fmode = (user_logic, user_logic)
        elif game_choice == 'mid':
            fmode = (user_logic, comp_logic)
        elif game_choice == 'bottom':
            fmode = (comp_logic, comp_logic)
        if bin_choice == 'white':
            faskr, fp1, fp2, fc = -1, 'White', 'Black', 1
        elif bin_choice == 'black':
            faskr, fp1, fp2, fc = 1, 'Black', 'White', 0
        return faskr, fp1, fp2, fc, fmode
    else:
        return bin_choice


def piece_generator(board):
    piece_rects = []
    piece_dict = {1: b_pawn, -1: w_pawn, 3: b_night, -3: w_night, 4: b_bishop, -4: w_bishop, 5: b_rook, -5: w_rook,
                  9: b_queen, -9: w_queen, 10: b_king, -10: w_king}
    for ix in range(8):
        for iy in range(8):
            if board[ix, iy] == 0:
                pass
            else:
                piece_map = piece_dict[board[ix, iy]]
                piece_rects.append([piece_map, piece_map.get_rect(topleft=(44 + 64 * iy, 44 + 64 * ix))])
    return piece_rects


def board_coor(topleft_coor):
    for coorx, xgrid in enumerate(grid):
        for coory, ygrid in enumerate(grid):
            if topleft_coor == (ygrid[0], xgrid[0]):
                return [coorx, coory]


def check_for_endings():
    global checkmate, three_rep, fifty_move
    game_boards.append([list(line) for line in Board])
    for pos in game_boards:
        if game_boards.count(pos) == 3:
            checkmate, three_rep = True, True
            break
    if len(moves_played.values()) > 50:
        valid_move = False
        for mv in list(moves_played.values())[-50:]:
            if 'x' in mv or mv[0] in playrmn:
                valid_move = True
                break
        if not valid_move:
            checkmate, fifty_move = True, True


def score_tracker():
    score = 0
    for row in Board:
        for value in row:
            score += value
    screen.blit(result_font.render(f'score: {int(-score)}', True, (255, 187, 130)), (760, 280))


def promotion(data):
    promo = ''
    location = data[-2]
    w_piece = [w_queen, w_rook, w_bishop, w_night]
    b_piece = [b_queen, b_rook, b_bishop, b_night]
    col = {0: w_piece, 7: b_piece} if askr == -1 else {7: w_piece, 0: b_piece}
    if location[0] == 0:
        promo_rect = promo_strip.get_rect(topleft=(44 + 64 * location[1], 44))
        steps = [44, 108, 172, 236]
    else:
        promo_rect = promo_strip.get_rect(bottomleft=(44 + 64 * location[1], 556))
        steps = [300, 364, 428, 492]
    promo_flip = pg.transform.flip(promo_strip, False, True) if location[1] in [1, 3, 5, 7] else promo_strip
    queen_rect = col[location[0]][0].get_rect(topleft=(44 + 64 * location[1], steps[0]))
    rook_rect = col[location[0]][1].get_rect(topleft=(44 + 64 * location[1], steps[1]))
    bishop_rect = col[location[0]][2].get_rect(topleft=(44 + 64 * location[1], steps[2]))
    night_rect = col[location[0]][3].get_rect(topleft=(44 + 64 * location[1], steps[3]))
    while not promo:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if (event.type == pg.MOUSEBUTTONDOWN) and (event.button == 1):
                if mouse_in_rect(queen_rect):
                    promo = 'Q'
                elif mouse_in_rect(rook_rect):
                    promo = 'R'
                elif mouse_in_rect(bishop_rect):
                    promo = 'B'
                elif mouse_in_rect(night_rect):
                    promo = 'N'
        screen.blit(back_ground, (0, 0))
        coor_display(askr)
        screen.blit(chess_board, chess_board_rect)
        for piece in all_pieces:
            p_type, p_rect = piece
            screen.blit(p_type, p_rect)
        screen.blit(dark_square, (44, 44))
        screen.blit(promo_flip, promo_rect)
        screen.blit(col[location[0]][0], queen_rect)
        screen.blit(col[location[0]][1], rook_rect)
        screen.blit(col[location[0]][2], bishop_rect)
        screen.blit(col[location[0]][3], night_rect)
        pg.display.update()
        clock.tick(120)
    return promo


def play_move(played_move, side, opp):
    global kingm, arm, hrm, kingm1, arm1, hrm1
    pro, promo, ch, move, oldp, rookdata, cch = '', '', '', '', '', '', []
    move, lgd = played_move
    xx0 = list(positions.values())[lgd[2]]

    if lgd[0] == pawns and Board[lgd[1][0], lgd[1][1]] == 0 and xx0[1] != lgd[1][1]:
        v = list(positions.values()).index(lgd[1])
        pawns[v - side * 8].col = 0

    if side == 1:
        rookdata = [3, 5] if player1 == 'White' else [2, 4]
        oldp = [7, 0]
    elif side == -1:
        rookdata = [59, 61] if player1 == 'White' else [58, 60]
        oldp = [63, 56]
    if (move == 'O-O' and player1 == 'White') or (move == 'O-O-O' and player1 == 'Black'):
        rooks[oldp[0]].col = 0
        rooks[rookdata[1]].col = 5 * side * askr
    elif (move == 'O-O-O' and player1 == 'White') or (move == 'O-O' and player1 == 'Black'):
        rooks[oldp[1]].col = 0
        rooks[rookdata[0]].col = 5 * side * askr

    newpiecepos(lgd[0], lgd[1], lgd[2])

    if lgd[0] == pawns and (lgd[1][0] == 0 or lgd[1][0] == 7):
        pawns[list(positions.values()).index(lgd[1])].col = 0
        prodata = {'Q': 9, 'R': 5, 'B': 4, 'N': 3}
        if opp == 'comp':
            pro = list(prodata.keys())[np.random.randint(len(prodata))]
        else:
            pro = promotion(lgd)
        for pco in pieces:
            if pro.lower() == str(pco[0])[0]:
                promo = pco
        promo[list(positions.values()).index(lgd[1])].col = prodata[pro] * side * askr

    game_moves.append([lgd[0][lgd[2]].pos(), lgd[1]])
    if check(-side * askr):
        ch = '+'
    moves_played.update({count: move + pro + ch})
    print(f'{count}: {move}{pro}{ch}')
    if lgd[0] == kings:
        if side == 1:
            kingm, arm, hrm = True, True, True
        elif side == -1:
            kingm1, arm1, hrm1 = True, True, True
    if lgd[0] == rooks:
        if side == 1:
            if rooks[lgd[2]].name[0] == 'a':
                arm = True
            if rooks[lgd[2]].name[0] == 'h':
                hrm = True
        if side == -1:
            if rooks[lgd[2]].name[0] == 'a':
                arm1 = True
            if rooks[lgd[2]].name[0] == 'h':
                hrm1 = True


def user_logic(side):
    condition = 0
    global mouse_piece, checkmate, count, attempted_mouse_move
    lgm, lgdata = list_move(side * askr)
    if not lgm:
        checkmate = True
        condition = 1
    while condition == 0:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if (event.type == pg.MOUSEBUTTONDOWN) and (event.button == 1):
                for pce in all_pieces:
                    ptype, prect = pce
                    if mouse_in_rect(prect):
                        mouse_piece = [all_pieces.index(pce), prect.topleft]
                        attempted_mouse_move.clear()
                        attempted_mouse_move.append(board_coor(prect.topleft))
                        break
            if (event.type == pg.MOUSEBUTTONUP) and (event.button == 1) and (mouse_piece[0] != ''):
                mouse_rect = all_pieces[mouse_piece[0]]
                old_position = mouse_piece[1]
                if not mouse_in_rect(chess_board_rect):
                    mouse_rect[1].topleft = old_position
                    mouse_piece = ['', '']
                else:
                    xm, ym = pg.mouse.get_pos()
                    for ig in grid:
                        for jg in grid:
                            if (ig[0] <= xm <= ig[1]) and (jg[0] <= ym <= jg[1]):
                                verdict = 'not legal'
                                attempted_mouse_move.append(board_coor((ig[0], jg[0])))
                                for lgd in lgdata:
                                    if [lgd[0][lgd[2]].pos(), lgd[1]] == attempted_mouse_move:
                                        verdict = (lgm[lgdata.index(lgd)], lgd)
                                if verdict == 'not legal':
                                    mouse_rect[1].topleft = old_position
                                else:
                                    play_move(verdict, side, 'player')
                                    condition = 1
                                mouse_piece = ['', '']
        screen.blit(back_ground, (0, 0))
        coor_display(askr)
        screen.blit(chess_board, chess_board_rect)
        score_tracker()
        held_piece, held_type = 0, 0
        for piece in all_pieces:
            p_type, p_rect = piece
            if all_pieces.index(piece) != mouse_piece[0]:
                screen.blit(p_type, p_rect)
            else:
                held_piece, held_type = p_rect, p_type
        if held_piece != 0:
            held_piece.center = pg.mouse.get_pos()
            screen.blit(held_type, held_piece)
        pg.display.update()
        clock.tick(120)


def comp_logic(side):
    condition = 0
    global checkmate
    while condition == 0:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        screen.blit(back_ground, (0, 0))
        coor_display(askr)
        screen.blit(chess_board, chess_board_rect)
        score_tracker()
        for piece in all_pieces:
            p_type, p_rect = piece
            screen.blit(p_type, p_rect)
        pg.display.update()
        clock.tick(120)
        lgm, lgdata = list_move(side * askr)
        if not lgm:
            checkmate = True
            break
        move = np.random.choice(lgm)
        lgd = lgdata[lgm.index(move)]
        play_move((move, lgd), side, 'comp')
        condition = 1


while __name__ == '__main__':
    Board, playrmn = np.zeros(shape=(8, 8)), 'abcdefgh'
    grid = list(zip(range(44, 493, 64), range(108, 557, 64)))
    mouse_piece, attempted_mouse_move = ['', ''], []
    game_moves, moves_played, game_boards = [[[0, 0], [0, 0]]], {}, []
    kingm, kingm1, arm, hrm, arm1, hrm1 = False, False, False, False, False, False
    checkmate, three_rep, fifty_move = False, False, False

    askr, player1, player2, count, mode = options_display()

    z1 = {x + str(j + 1): [7 - j, playrmn.index(x)] for j in np.arange(8) for x in playrmn}
    positions = dict(zip(list(z1.keys())[::-askr], list(z1.values())))
    pawns, rooks = [x for x in positions.keys()], [x for x in positions.keys()]
    bishops, nights = [x for x in positions.keys()], [x for x in positions.keys()]
    queens, kings = [x for x in positions.keys()], [x for x in positions.keys()]
    pieces = [pawns, rooks, bishops, nights, queens, kings]

    start_piece()
    while not checkmate:
        time.sleep(0)
        all_pieces = piece_generator(update_board())
        count += 1
        if count % 2 == 0:
            mode[0](1)
        else:
            mode[1](-1)
        check_for_endings()

    if three_rep:
        message = 'Draw by repetition'
    elif fifty_move:
        message = 'Draw by fifty-move rule'
    elif check(-askr):
        message = f'Checkmate, {player1} is victorious!'
    elif check(askr):
        message = f'Checkmate, {player2} is victorious!'
    else:
        message = 'Stalemate'
    keep_playing = options_display(message)
    if keep_playing == 'quit':
        sys.exit()
