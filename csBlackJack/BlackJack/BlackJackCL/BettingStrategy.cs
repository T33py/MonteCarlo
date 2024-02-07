using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BlackJackCL
{
    public class BettingStrategy
    {
        public int On1 { get; set; } = 10;
        public int On2 { get; set; } = 10;
        public int On3 { get; set; } = 10;
        public int On4 { get; set; } = 10;
        public int On5 { get; set; } = 10;
        public int On6 { get; set; } = 10;
        public int On7 { get; set; } = 10;
        public int On8 { get; set; } = 10;
        public int On9 { get; set; } = 10;
        public int On10OrAbove { get; set; } = 10;

        public int Bet(int count)
        {
            int bet = 10;

            switch (count)
            {
                case 1:
                    bet = On1;
                    break;
                case 2:
                    bet = On2;
                    break;
                case 3:
                    bet = On3;
                    break;
                case 4:
                    bet = On4;
                    break;
                case 5:
                    bet = On5;
                    break;
                case 6:
                    bet = On6;
                    break;
                case 7:
                    bet = On7;
                    break;
                case 8:
                    bet = On8;
                    break;
                case 9:
                    bet = On9;
                    break;
                case >= 10:
                    bet = On10OrAbove;
                    break;

                default: break;
            }

            return bet;
        }

        public override string ToString()
        {
            return $"1: {On1}, 2: {On2}, 3: {On3}, 4: {On4}, 5: {On5}, 6: {On6}, 7: {On7}, 8: {On8}, 9: {On9}, >=10: {On10OrAbove}, ";
        }
    }
}
