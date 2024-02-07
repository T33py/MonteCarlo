using BlackJack;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BlackJackCL
{
    public class BlackJackWrapper
    {
        public Game BlackJack { get; set; } = new Game(6);

        public int MaxRounds { get; set; } = 10000000;
        int round = 0;
        
        public Dictionary<IPlayer,  SimulationResult> PlayerResultMap { get; set; }

        public List<IPlayer> Players { get => BlackJack.Players; }


        public BlackJackWrapper() 
        {
            ResetToDefaults();
        }

        public void ResetToDefaults()
        {
            BlackJack = new Game(6);

            BlackJack.AddPlayer(new CardCounter(0));

            round = 0;
            PlayerResultMap = new Dictionary<IPlayer, SimulationResult>();
        }

        public void RunSimulation()
        {

            //while (game.player.Money > 0 && rounds != maxRounds)
            //Console.WriteLine("Running games");
            while (round != MaxRounds)
            {
                BlackJack.PlayRound();
                round++;
            }
            //Console.WriteLine("Ended games");

            var players = BlackJack.Players;

            foreach (var p in players)
            {
                float endingMoney = p.Money;
                float diff = endingMoney - p.StartingMoney;
                float lossP = (diff / p.AllBetTotal) * 100;
                float pr = diff / round;

                var result = new SimulationResult();
                result.Player = p;
                result.EndingMoney = endingMoney;
                result.DifferenceInBalance = diff;
                result.LossInPercent = lossP;
                result.AverageBalanceChangePerRound = pr;
                result.Rounds = round;


                PlayerResultMap.Add(p, result);

                //Console.WriteLine(result.ToString());
                
            }
        }
    }
}
