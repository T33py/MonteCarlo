using BlackJack;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BlackJackCL
{
    public class SimplePlayer : IPlayer
    {
        public string Name { get; set; } = "Simpleton";
        int money = 100000;
        public int Money { get => money; set => money = value; }

        public float AllBetTotal { get; set; } = 0;

        public List<Hand> Hands { get; set; } = new List<Hand>();
        public int StartingMoney { get; set; } = 100000;

        public int Bet()
        {
            int bet = 10;
            AllBetTotal += bet;
            return bet;
        }

        public bool DoubleDown(Hand hand, Card dealerShows)
        {
            return false;
        }

        public bool Hit(Hand hand, Card dealerShows)
        {
            if (hand.Value < 18)
            {
                //Console.WriteLine("  HIT");
                return true;
            }
            return false;
        }

        public int PlayHands()
        {
            return 1;
        }

        public void Result(Hand dealersHand, int totalPayout)
        {
            //Console.WriteLine($"P: {Hands[0]} | D: {dealersHand} | {Hands[0].CurrentState} | {Hands[0].Value} v {dealersHand.Value}  => {money}");
            //Console.ReadLine();
        }

        public bool Split(Hand hand, Card dealerShows)
        {
            return false;
        }

        public void OnShuffle()
        {
            
        }

        public void OnCardDealt(Card card, bool faceDown)
        {
            
        }
    }
}
