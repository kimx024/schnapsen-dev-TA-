import random
from typing import Optional
from schnapsen.game import Bot, PlayerPerspective, Move, SchnapsenTrickScorer, RegularMove
from schnapsen.deck import Card, Suit


class BullyBot(Bot):
    def __init__(self) -> None:
        pass

    def get_move(self, player_perspective: PlayerPerspective, leader_move: Optional[Move], ) -> Move:
        # The bully bot only plays valid moves.

        # initialize variables to get all valid moves.
        # also, keep track of all the trump suit moves; this is going to be a list of object Move,
        # that is a class within game.py
        my_valid_moves = player_perspective.valid_moves()
        trump_suit_moves: list[Move] = []

        # initialize a variable to get the trump suit
        trump_suit: Suit = player_perspective.get_trump_suit()

        # get all my valid moves that have the same suit with trump suit.
        for move in my_valid_moves:
            cards_of_move: list[Card] = move.cards
            # get 1st of the list of cards of this move (in case of multiple -> Marriage)
            card_of_move: Card = cards_of_move[0]

            if card_of_move.suit == trump_suit:
                trump_suit_moves.append(move)

        # If you have cards of the trump suit, play one of them at random
        if len(trump_suit_moves) > 0:
            random_trump_suit_move = random.choice(trump_suit_moves)
            return random_trump_suit_move

        # Else, if you are the follower, and
        # you have cards of the same suit as the opponent, play one of these at random.
        if not player_perspective.am_i_leader():
            assert leader_move is not None
            leader_suit: Suit = leader_move.cards[0].suit
            leaders_suit_moves: list[Move] = []

            # get all my valid moves that have the same suit with trump suit.
            for move in my_valid_moves:
                cards_of_move: list[Card] = move.cards
                # get 1st of the list of cards of this move (in case of multiple -> Marriage)
                card_of_move: Card = cards_of_move[0]

                if card_of_move.suit == leader_suit:
                    leaders_suit_moves.append(move)

            if len(leaders_suit_moves) > 0:
                random_leader_suit_move = random.choice(leaders_suit_moves)
                return random_leader_suit_move

        # Else, play one of your cards with the highest rank
        # get the list of cards in my hand
        my_hand_cards: list[Card] = list(player_perspective.get_hand().cards)

        # create an instance object of a SchnapsenTrickScorer Class,
        # that allows us to get the rank of Cards.
        schnapsen_trick_scorer = SchnapsenTrickScorer()
        # we set the highest rank to something negative,
        # forcing it to change with the first comparison, since all scores are
        highest_card_score: int = -1
        card_with_highest_score: Optional[Card] = None
        for card in my_hand_cards:
            card_score = schnapsen_trick_scorer.rank_to_points(card.rank)
            if card_score > highest_card_score:
                highest_card_score = card_score
                card_with_highest_score = card

        # if our logic above was correct, this can never be None. We double check to make sure.
        assert card_with_highest_score is not None
        move_of_card_with_highest_score = RegularMove(card_with_highest_score)

        # We can double-check that this is a valid move like this.
        assert move_of_card_with_highest_score in my_valid_moves

        return move_of_card_with_highest_score
