using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BlackJack
{
    public interface IPlayer
    {
        /// <summary>
        /// The name to display for this player
        /// </summary>
        public string Name { get; set; }

        /// <summary>
        /// The  running total for the player
        /// </summary>
        public int Money { get; set; }

        /// <summary>
        /// The starting balance for the player
        /// </summary>
        public int StartingMoney { get; set; }

        /// <summary>
        /// The sum total of all bets
        /// </summary>
        public float AllBetTotal { get; set; }

        /// <summary>
        /// The current hands being played by the player
        /// </summary>
        public List<Hand> Hands { get; set; }

        /// <summary>
        /// Number of hands the player will play at the table in the round about to be dealt
        /// </summary>
        /// <returns>Number of hands to bet on</returns>
        public int PlayHands();

        /// <summary>
        /// The ammount of money that will be bet on the hand currently being asked for a bet
        /// </summary>
        /// <returns></returns>
        public int Bet();

        /// <summary>
        /// Whether the player wants to hit on the hand provided
        /// </summary>
        /// <param name="hand">Hand for the player to decide on</param>
        /// <param name="dealerShows">The card showin for the dealer</param>
        /// <returns>Yes or no</returns>
        public bool Hit(Hand hand, Card dealerShows);

        /// <summary>
        /// Whether the player wants to double down on the hand provided
        /// </summary>
        /// <param name="hand">Hand for the player to decide on</param>
        /// <param name="dealerShows">The card showin for the dealer</param>
        /// <returns>Yes or no</returns>
        public bool DoubleDown(Hand hand, Card dealerShows);

        /// <summary>
        /// Whether the player wants to split on the hand provided
        /// </summary>
        /// <param name="hand">Hand for the player to decide on</param>
        /// <param name="dealerShows">The card showin for the dealer</param>
        /// <returns>Yes or no</returns>
        public bool Split(Hand hand, Card dealerShows);

        /// <summary>
        /// This method is called whenever a game of blackjack ends
        /// </summary>
        /// <param name="dealersHand">The hand the dealer ended with</param>
        /// <param name="totalPayout">The total won or lost for the player</param>
        public void Result(Hand dealersHand, int totalPayout);

        /// <summary>
        /// This function is called when the deck is shuffled
        /// </summary>
        public void OnShuffle();

        /// <summary>
        /// This function is called whenever a card is taken from the deck
        /// </summary>
        /// <param name="card">The card that was dealt</param>
        /// <param name="faceDown">Whether this card was dealt face down</param>
        public void OnCardDealt(Card card, bool faceDown);
    }
}
