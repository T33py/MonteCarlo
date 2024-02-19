using OneArmedBandit;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BanditSimulation
{
    public class SimpleBandit : Bandit
    {
        public override string Name { get; set; } = "Simple bandit";
        public override List<int> Symbols { get; set; } = new List<int>() { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 };
        public override List<Wheel> Wheels { get; set; } = new List<Wheel>();
        public override int Lines { get; set; } = 1;
        public override int LinesAvailable { get => lines.Count; }
        public override int BetPerLine { get; set; } = 1;
        int balance = 0;
        public override int CurrentBalance { get => balance; }
        public int LastOutcome { get; set; } = 0;

        List<int[]> lines = new List<int[]>() { 
            new int[] { 0, 0, 0, 0, 0 },
            new int[] { 1, 1, 1, 1, 1 },
            new int[] { 2, 2, 2, 2, 2 },
            new int[] { 0, 1, 2, 1, 0 },
            new int[] { 1, 0, 1, 0, 1 },
            new int[] { 1, 2, 1, 0, 1 },
            new int[] { 1, 0, 1, 0, 1 },
            new int[] { 1, 2, 1, 2, 1 },
            new int[] { 2, 1, 2, 1, 2 },
            new int[] { 2, 1, 0, 1, 2 },
        };

        bool rolling = false;
        int w5 = 0;

        long totalWagered = 0;
        long totalPayout = 0;

        public SimpleBandit()
        {
            for (int i = 0; i < 5; i++)
            {
                Wheels.Add(new Wheel(this));
            }
            for (int i = 0; i < Wheels[0].ShowsSymbols; i++)
            {
                foreach (Wheel w in Wheels)
                {
                    w.Spin();
                }
            }
            Lines = lines.Count;
        }

        public override int CashOut()
        {
            var cash = balance; 
            balance = 0; 
            return cash;
        }

        public override void InsertCoins(int ammount)
        {
            balance += ammount;
        }

        public override void ForceSymbols(Wheel wheel)
        {
            // todo
        }

        public override List<int> GetAllowedSymbols()
        {
            return Symbols;
        }

        public override int NextSymbol(Wheel wheel)
        {
            return 0;
        }

        public override void Pull()
        {
            if (rolling) return;
            if (Lines > lines.Count) return;
            var wager = BetPerLine * Lines;
            balance -= wager;
            totalWagered += wager;
            w5 = 0;
            rolling = true;
        }

        public override void Roll()
        {
            if (!rolling) return;

            Wheels[4].Spin();
            w5 += 1;

            if (w5 % 2 == 0)
            {
                Wheels[3].Spin();
            }

            if (w5 % 3 == 0)
            {
                Wheels[2].Spin();
            }

            if (w5 % 4 == 0)
            {
                Wheels[1].Spin();
            }

            if (w5 % 5 == 0)
            {
                Wheels[0].Spin();
            }
        }

        public override int EndRoll()
        {
            if (!rolling) return 0;
            rolling = false;
            var res = 0;
            for (int i = 0; i < Lines; i++)
            {
                res += DetermineOutcome(lines[i]);
            }
            LastOutcome = res;
            balance += res;
            totalPayout += res;
            return res;
        }

        int DetermineOutcome(int[] line)
        {
            // if wheel 1 matches wheel 2
            if (Wheels[0].Symbols[line[0]] == Wheels[1].Symbols[line[1]])
            {

                // if wheel 2 matches wheel 3
                if (Wheels[1].Symbols[line[1]] == Wheels[2].Symbols[line[2]])
                {

                    // if wheel 3 matches wheel 4
                    if (Wheels[2].Symbols[line[2]] == Wheels[3].Symbols[line[3]])
                    {

                        // if wheel 4 matches wheel 5
                        if (Wheels[3].Symbols[line[3]] == Wheels[4].Symbols[line[4]])
                        {
                            //Console.WriteLine(ToString());
                            //Console.WriteLine((Wheels[0].Symbols[line[0]] + BetPerLine) * 100);
                            //Console.ReadLine();
                            return ((Wheels[0].Symbols[line[0]]+1) * BetPerLine) * 100;
                        }
                        return ((Wheels[0].Symbols[line[0]] + 1) * BetPerLine) * 40;
                    }
                    return ((Wheels[0].Symbols[line[0]] + 1) * BetPerLine) * 10;
                }
                return ((Wheels[0].Symbols[line[0]] + 1) * BetPerLine) / 2;
                
            }

            return 0;
        }

        public override string? ToString()
        {
            var str = "";
            for (int i = 0; i < Wheels[0].ShowsSymbols; i++)
            {
                foreach (var w in Wheels)
                {
                    str += w.Symbols[i] + " ";
                }
                str += "\n";
            }

            str += "\n";
            str += $"Current Balance: {CurrentBalance}  |  Win: {LastOutcome}  |  Bet: {BetPerLine * Lines}\n";

            float retp = 0;
            if (totalWagered > 0)
                retp = ((float)totalPayout / (float)totalWagered) * 100;
            str += $"Total wagered: {totalWagered}  |  Total payout: {totalPayout}  |  return: {retp:0.00}%";

            return str;
        }
    }
}
