using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;

namespace BlackJack
{
    public class Hand
    {
        public int Bet {  get; set; } = 0;
        public List<Card> Cards { get; set; } = new List<Card>();
        public State CurrentState { get; set; } = Hand.State.Playing;
        public bool doubled = false;
        public int Value { get => CalculateValue(); }
        public bool HasAce { get => IsAce_(); }
        public bool IsPair { get => IsPair_(); }
        bool isSoft = false;
        public bool IsSoft { get => IsSoft_(); }

        public int CalculateValue() 
        {
            int val = 0;
            int aces = 0;
            foreach (var card in Cards)
            {
                val += card.value;
                if (card.Symbol.Equals("A"))
                {
                    aces++;
                    isSoft = true;
                }
                // aces turn into 1s when the hand is bust
                while (val > 21 && aces > 0)
                {
                    val -= 10;
                    aces -= 1;
                }
            }

            // if there is any aces left the total is soft
            if (aces > 0)
            {
                isSoft = true;
            }
            else
            {
                isSoft = false;
            }
            return val; 
        }

        public bool CanSplit()
        {
            if (Cards.Count != 2)
                return false;
            if (Cards[0].Symbol.Equals(Cards[1].Symbol))
                return true;
            return false;
        }

        public bool CanDouble()
        {
            if (Cards.Count == 2)
            {
                return true;
            }
            return false;
        }

        public enum State
        {
            Playing,
            Stands,
            Bust,
            Lost,
            Push,
            Won,
            BlackJack,
        }

        public override string ToString()
        {
            var cardss = "";
            foreach (var card in Cards)
            {
                cardss += card.ToString() + ", ";
            }
            cardss = cardss.Substring(0, cardss.Length - 2);
            return $"{cardss}";
        }

        bool IsAce_()
        {
            foreach (var card in Cards)
            {
                if (card.IsAce) return true;
            }
            return false;
        }

        bool IsPair_()
        {
            if (Cards.Count == 2)
            {
                if (Cards[0].Symbol.Equals(Cards[1].Symbol)) return true;
            }
            return false;
        }

        bool IsSoft_()
        {
            CalculateValue();
            return isSoft;
        }
    }
}
