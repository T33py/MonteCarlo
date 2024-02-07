using BlackJack;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BlackJackCL
{
    public class SlightlySmarterPlayer : IPlayer
    {
        public bool shouldDouble = true;
        public bool shouldSplit = true;
        public int standOn = 16;
        public bool pauseNext = false;

        public string Name { get; set; } = "Not that smart";
        int money = 100000;
        public int Money { get => money; set => money = value; }

        public float AllBetTotal { get; set; } = 0;

        public int StartingMoney { get; set; }

        public List<Hand> Hands { get; set; } = new List<Hand>();


        public SlightlySmarterPlayer(int startingMoney) 
        { 
            this.StartingMoney = startingMoney;
            money = startingMoney;
        }

        public int Bet()
        {
            int bet = 10;
            AllBetTotal += bet;
            return bet;
        }

        public bool Split(Hand hand, Card dealerShows)
        {
            if (!shouldSplit) return false;

            if (hand.CanSplit())
            {
                if (hand.Cards[0].IsAce && hand.Cards[1].IsAce)
                {
                    //Console.WriteLine($"P: {hand} | D: {dealerShows} | SPLIT");
                    //pauseNext = true;
                    return true;
                }

            }
            return false;
        }

        public bool DoubleDown(Hand hand, Card dealerShows)
        {
            if (!shouldDouble) return false;

            if (hand.Value == 10 ||  hand.Value == 11)
            {
                return true;
            }
            return false;
        }

        public bool Hit(Hand hand, Card dealerShows)
        {
            if (hand.Value < standOn)
            {
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
            if (pauseNext)
            {
                pauseNext = false;
                for (int i = 0; i < Hands.Count; i++)
                {
                    Console.WriteLine($"P: {Hands[i]} | D: {dealersHand} | {Hands[i].CurrentState} | {Hands[i].Value} v {dealersHand.Value}  => {money}");
                }
                Console.ReadLine();
            } 
        }

        public void OnShuffle()
        {
            
        }

        public void OnCardDealt(Card card, bool faceDown)
        {
            
        }
    }
}
