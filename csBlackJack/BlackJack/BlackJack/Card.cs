using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BlackJack
{
    public class Card
    {
        public static string[] Symbols = new string[] { "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K" };
        public static string[] Suits = new string[] { "H", "K", "S", "D" };
        public static Dictionary<string, int> CardValues = new Dictionary<string, int>
        {
            { "A", 11 },
            { "2", 2 },
            { "3", 3 },
            { "4", 4 },
            { "5", 5 },
            { "6", 6 },
            { "7", 7 },
            { "8", 8 },
            { "9", 9 },
            { "10", 10 },
            { "J", 10 },
            { "Q", 10 },
            { "K", 10 },
        };

        public string Symbol { get; }
        public string Suit {  get; }
        public int value { get => CardValues[Symbol]; }

        public bool IsAce { get => Symbol.Equals("A"); }
        public bool IsTwo { get => Symbol.Equals("2"); }
        public bool IsThree { get => Symbol.Equals("3"); }
        public bool IsFour { get => Symbol.Equals("4"); }
        public bool IsFive { get => Symbol.Equals("5"); }
        public bool IsSix { get => Symbol.Equals("6"); }
        public bool IsSeven { get => Symbol.Equals("7"); }
        public bool IsEight { get => Symbol.Equals("8"); }
        public bool IsNine { get => Symbol.Equals("9"); }
        public bool IsTen { get => Symbol.Equals("10"); }
        public bool IsJack { get => Symbol.Equals("J"); }
        public bool IsQeen { get => Symbol.Equals("Q"); }
        public bool IsKing { get => Symbol.Equals("K"); }


        public Card(string Symbol, string Suit) 
        {
            this.Symbol = Symbol;
            this.Suit = Suit;
        }

        public override string ToString()
        {
            return $"{Symbol}-{Suit}";
        }
    }
}
