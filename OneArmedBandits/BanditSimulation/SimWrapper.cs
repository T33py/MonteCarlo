using OneArmedBandit;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BanditSimulation
{
    public class SimWrapper
    {
        bool Stop {  get; set; } = false;
        SimpleBandit bandit = new SimpleBandit();

        public void Run()
        {
            //bandit.Lines = 3;
            bandit.BetPerLine = 10;
            //Console.WriteLine($"Welcome to {bandit.Name}");
            Display();
            int spins = 0;
            while (!Stop)
            {
                //Display();
                //Console.ReadLine();
                Spin();
                spins++;
                if (spins % 10000 == 0)
                {
                    Display();
                    Console.WriteLine($"spins: {spins}");
                    Console.ReadLine();
                    //Thread.Sleep(10);
                }
            }
        }

        public void Spin() 
        {
            bandit.Pull();

            for ( int i = 0;i < 30;i++ )
            {
                bandit.Roll();
            }

            bandit.EndRoll();

        }

        public void Display()
        {
            Console.Clear();
            Console.CursorLeft = 0;
            Console.CursorTop = 0;
            Console.WriteLine($"Welcome to {bandit.Name}");
            Console.WriteLine(bandit.ToString());
        }
    }
}
