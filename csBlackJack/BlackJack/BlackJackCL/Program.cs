// See https://aka.ms/new-console-template for more information
using BlackJack;
using BlackJackCL;
using System.Runtime.InteropServices;


BlackJackWrapper blSim = new BlackJackWrapper();
blSim.MaxRounds = 1000000;

Dictionary<BettingStrategy, SimulationResult> fallout = new Dictionary<BettingStrategy, SimulationResult>();

for (int i1 = 10; i1 < 50; i1 += 10)
{
    Console.WriteLine(i1 + "/" + 50);
    for (int i3 = i1 + 10; i3 < 60; i3 += 10)
    {
        for (int i5 = i3 + 10; i5 < 110; i5 += 10)
        {
            for (int i7 = i5 + 10; i7 < 110; i7 += 10)
            {
                BettingStrategy strategy = new BettingStrategy();
                strategy.On1 = i1;
                strategy.On2 = i1;
                strategy.On3 = i3;
                strategy.On4 = i3;
                strategy.On5 = i5;
                strategy.On6 = i5;
                strategy.On7 = i7;
                strategy.On8 = i7;
                strategy.On9 = i7;
                strategy.On10OrAbove = i7;

                ((CardCounter)blSim.Players[0]).BettingStrategy = strategy;

                blSim.RunSimulation();
                var res = blSim.PlayerResultMap[blSim.Players[0]];

                fallout.Add(strategy, res);

                blSim.ResetToDefaults();
            }
        }
    }
    PrintBest();
}

void PrintBest()
{
    var top10 = new Dictionary<BettingStrategy, SimulationResult>();
    foreach(var strat in fallout.Keys)
    {
        bool nxt = false;
        var res = fallout[strat];
        if (top10.Count < 10)
        {
            top10.Add(strat, res);
            nxt = true;
            continue;
        }

        var ks = new List<BettingStrategy>(top10.Keys);
        for (int i = 0; i < ks.Count; i++) 
        { 
            if (nxt)
                break;

            if (top10[ks[i]].EndingMoney < res.EndingMoney)
            {
                top10.Remove(ks[i]);
                top10.Add(strat, res);
                nxt = true;
                break;
            }
        }
    }



    foreach (var strat in top10.Keys)
    {
        Console.WriteLine(strat.ToString());
        Console.WriteLine(top10[strat].ToString());
        Console.WriteLine();
    }
}


//for (int i = 15; i < 19; i++)
//{
//    var p = new SlightlySmarterPlayer(100000);
//    players.Add(p);
//    p.standOn = i;
//    p.Name = $"Stands on {i}";
//    game.BlackJack.AddPlayer(p);
//}


