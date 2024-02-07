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
        

        public BlackJackWrapper() 
        {
            ResetToDefaults();
        }

        public void ResetToDefaults()
        {
            BlackJack = new Game(6);

            //BlackJack.AddPlayer(player);
            BlackJack.AddPlayer(new CardCounter(100000));
            var _p = new PerfectBasicStrategyPlayer(100000);
            BlackJack.AddPlayer(_p);
            //Console.WriteLine(_p.PrintStrategy());
            var _sp = new SlightlySmarterPlayer(100000);
            _sp.standOn = 16;
            BlackJack.AddPlayer(_sp);
            BlackJack.AddPlayer(new SimplePlayer());

            round = 0;
        }


        public void RunSimulation()
        {

            //while (game.player.Money > 0 && rounds != maxRounds)
            Console.WriteLine("Running games");
            while (round != MaxRounds)
            {
                BlackJack.PlayRound();
                round++;
            }
            Console.WriteLine("Ended games");

            var players = BlackJack.Players;

            foreach (var p in players)
            {
                float endingMoney = p.Money;
                float diff = endingMoney - p.StartingMoney;
                float lossP = (diff / p.AllBetTotal) * 100;
                float pr = diff / round;
                Console.WriteLine($"{p.Name}:");
                Console.WriteLine($"  Ended with {endingMoney} after {round} rounds");
                Console.WriteLine($"  Edge is {lossP:0.00}%");
                Console.WriteLine($"     netting {pr} per round");
            }
        }
    }
}
