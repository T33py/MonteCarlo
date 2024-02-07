using BlackJack;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BlackJackCL
{
    public class SimulationResult
    {
        public IPlayer? Player;
        public float EndingMoney;
        public float DifferenceInBalance;
        public float LossInPercent;
        public float AverageBalanceChangePerRound;
        public int Rounds;

        public override string ToString()
        {
            return
                $"{Player?.Name}:\n" +
                $"  Ended with {EndingMoney} after {Rounds} rounds\n" +
                $"  Edge is {LossInPercent:0.00}%\n" +
                $"  netting {AverageBalanceChangePerRound:0.000} per round";
        }
    }
}
