using BlackJack;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BlackJackCL
{
    public class CardCounter: IPlayer
    {
        public bool pauseNext = false;

        //    total incl. ace      dealers card
        Dictionary<int, Dictionary<string, string>> SoftTotalsRules = new Dictionary<int, Dictionary<string, string>>();
        //        total           dealers card
        Dictionary<int, Dictionary<string, string>> HardTotalsRules = new Dictionary<int, Dictionary<string, string>>();
        //        pair of          dealers card
        Dictionary<int, Dictionary<string, bool>> PairRules = new Dictionary<int, Dictionary<string, bool>>();

        public string Name { get; set; } = "Card Counter";
        int money = 100000;
        public int Money { get => money; set => money = value; }

        public float AllBetTotal { get; set; } = 0;

        public int StartingMoney { get; set; }

        public List<Hand> Hands { get; set; } = new List<Hand>();

        public int count = 0;

        public BettingStrategy BettingStrategy { get; set; } = new BettingStrategy();

        public CardCounter(int startingMoney)
        {
            this.StartingMoney = startingMoney;
            money = startingMoney;
            for (int i = 2; i <= 11; i++)
            {
                PairRules.Add(i, new Dictionary<string, bool>());
            }
            for (int i = 0; i <= 22; i++)
            {
                HardTotalsRules[i] = new Dictionary<string, string>();
                SoftTotalsRules[i] = new Dictionary<string, string>();
            }

            // Setup rules spreadsheet
            foreach (var s in new string[] { "2", "3", "4", "5", "6", "7", "8", "9", "10", "11" })
            {
                foreach (var htr in HardTotalsRules.Keys)
                {
                    HardTotalsRules[htr][s] = "H";

                }
                foreach (var str in SoftTotalsRules.Keys)
                {
                    SoftTotalsRules[str][s] = "H";
                }
                foreach (var p in PairRules.Keys)
                {
                    PairRules[p][s] = false;
                }
            }

            SetupHardTotalRules();
            SetupSoftTotalRules();
            SetupPairRules();
        }

        public int Bet()
        {
            int bet = BettingStrategy.Bet(count);
            AllBetTotal += bet;
            return bet;
        }

        public bool Split(Hand hand, Card dealerShows)
        {
            if (hand.IsPair)
            {
                return PairRules[hand.Cards[0].value][dealerShows.value.ToString()];
            }
            return false;
        }

        public bool DoubleDown(Hand hand, Card dealerShows)
        {
            if (hand.IsSoft)
            {
                if (SoftTotalsRules[hand.Value][dealerShows.value.ToString()].Equals("D")) return true;
            }
            else
            {
                if (HardTotalsRules[hand.Value][dealerShows.value.ToString()].Equals("D")) return true;
            }
            return false;
        }

        public bool Hit(Hand hand, Card dealerShows)
        {
            if (hand.IsSoft)
            {
                if (SoftTotalsRules[hand.Value][dealerShows.value.ToString()].Equals("H")) return true;
            }
            else
            {
                if (HardTotalsRules[hand.Value][dealerShows.value.ToString()].Equals("H")) return true;
            }
            return false;
        }

        public int PlayHands()
        {
            return 1;
        }

        public void Result(Hand dealersHand, int totalPayout)
        {
            OnCardDealt(dealersHand.Cards[0], false);
            if (pauseNext)
            {
                //pauseNext = false;
                for (int i = 0; i < Hands.Count; i++)
                {
                    Console.WriteLine($"P: {Hands[i]} | D: {dealersHand} | {Hands[i].CurrentState} | {Hands[i].Value} v {dealersHand.Value} | count: {count}");
                }
                Console.ReadLine();
            }
        }

        void SetupHardTotalRules()
        {
            var dcs = "2345678910A";
            foreach (var t in HardTotalsRules.Keys)
            {
                foreach (var dc in HardTotalsRules[t].Keys)
                {
                    if (t >= 17) HardTotalsRules[t][dc] = "S";
                    else if (t >= 13 && t <= 16 && dcs.Substring(0, 5).Contains(dc)) HardTotalsRules[t][dc] = "S";
                    else if (t == 12 && dcs.Substring(1, 4).Contains(dc)) HardTotalsRules[t][dc] = "S";
                    else if (t == 11) HardTotalsRules[t][dc] = "D";
                    else if (t == 10 && dcs.Substring(0, 8).Contains(dc)) HardTotalsRules[t][dc] = "D";
                    else if (t == 9 && dcs.Substring(1, 4).Contains(dc)) HardTotalsRules[t][dc] = "D";

                }
            }
        }

        void SetupSoftTotalRules()
        {
            var dcs = "2345678910A";
            foreach (var t in SoftTotalsRules.Keys)
            {
                foreach (var dc in SoftTotalsRules[t].Keys)
                {
                    if (t >= 19) SoftTotalsRules[t][dc] = "S";
                    else if (t == 19 && dc.Equals("6")) SoftTotalsRules[t][dc] = "D";
                    else if (t == 18 && dcs.Substring(0, 5).Contains(dc)) SoftTotalsRules[t][dc] = "D";
                    else if (t == 18 && dcs.Substring(5, 1).Contains(dc)) SoftTotalsRules[t][dc] = "S";
                    else if (t == 17 && dcs.Substring(1, 4).Contains(dc)) SoftTotalsRules[t][dc] = "D";
                    else if (t == 16 && dcs.Substring(2, 3).Contains(dc)) SoftTotalsRules[t][dc] = "D";
                    else if (t == 15 && dcs.Substring(2, 3).Contains(dc)) SoftTotalsRules[t][dc] = "D";
                    else if (t == 14 && dcs.Substring(3, 2).Contains(dc)) SoftTotalsRules[t][dc] = "D";
                    else if (t == 13 && dcs.Substring(3, 2).Contains(dc)) SoftTotalsRules[t][dc] = "D";
                }
            }
        }

        void SetupPairRules()
        {
            var dcs = "2345678910A";
            foreach (var v in PairRules.Keys)
            {
                foreach (var dc in PairRules[v].Keys)
                {
                    if (v == 11) PairRules[v][dc] = true;
                    if (v == 9 && dcs.Substring(0, 4).Contains(dc)) PairRules[v][dc] = true;
                    if (v == 8 && dcs.Substring(7, 1).Contains(dc)) PairRules[v][dc] = true;
                    if (v == 7) PairRules[v][dc] = true;
                    if (v == 6 && dcs.Substring(1, 3).Contains(dc)) PairRules[v][dc] = true;
                    if (v == 3 && dcs.Substring(2, 3).Contains(dc)) PairRules[v][dc] = true;
                    if (v == 2 && dcs.Substring(2, 3).Contains(dc)) PairRules[v][dc] = true;
                }
            }
        }

        public string PrintStrategy()
        {
            List<List<string>> lines = new List<List<string>>();
            lines.Add(new List<string>() { "Hard Totals:" });
            lines.Add(new List<string>() { "    2 3 4 5 6 7 8 9 10 11" });
            foreach (var t in HardTotalsRules.Keys.Reverse())
            {
                var tp = t.ToString();
                if (tp.Length == 1) tp += " ";
                var htr = new List<string>() { tp + ": " };
                lines.Add(htr);
                foreach (var dc in HardTotalsRules[t].Keys)
                {
                    htr.Add(HardTotalsRules[t][dc] + " ");
                }
            }
            lines.Add(new List<string>() { "Soft Totals:" });
            lines.Add(new List<string>() { "    2 3 4 5 6 7 8 9 10 11" });
            foreach (var t in SoftTotalsRules.Keys.Reverse())
            {
                var tp = t.ToString();
                if (tp.Length == 1) tp += " ";
                var str = new List<string>() { tp + ": " };
                lines.Add(str);
                foreach (var dc in SoftTotalsRules[t].Keys)
                {
                    str.Add(SoftTotalsRules[t][dc] + " ");
                }
            }

            string print = "";

            foreach (var l in lines)
            {
                var lp = "";
                foreach (var s in l)
                {
                    lp += s;
                }
                print += lp + "\n";
            }

            return print;
        }

        public void OnShuffle()
        {
            count = 0;
        }

        public void OnCardDealt(Card card, bool faceDown)
        {
            if (faceDown)
            {
                return;
            }

            if (card.value < 7) count += 1;
            if (card.value > 9) count -= 1;
        }
    }
}
