// See https://aka.ms/new-console-template for more information
using BlackJack;
using BlackJackCL;
using System.Runtime.InteropServices;


BlackJackWrapper blSim = new BlackJackWrapper();

int runs = 1;
for (int i = 0; i < runs; i++)
{
    Console.WriteLine($"Run {i+1}/{runs}");
    blSim.RunSimulation();
    blSim.ResetToDefaults();
}

//for (int i = 15; i < 19; i++)
//{
//    var p = new SlightlySmarterPlayer(100000);
//    players.Add(p);
//    p.standOn = i;
//    p.Name = $"Stands on {i}";
//    game.BlackJack.AddPlayer(p);
//}


