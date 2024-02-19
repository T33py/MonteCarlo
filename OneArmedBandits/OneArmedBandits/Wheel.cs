using System;
using System.Collections.Generic;
using System.Diagnostics.SymbolStore;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace OneArmedBandit
{
    /// <summary>
    /// Represents one of the spinning wheels of the slot machine
    /// </summary>
    public class Wheel
    {
        /// <summary>
        /// Number of symbols to display
        /// </summary>
        public int ShowsSymbols { get; set; } = 3;

        /// <summary>
        /// The symbols currently displayed on this wheel
        /// </summary>
        public List<int> Symbols { get; set; } = new List<int>();

        Random random = new Random();
        Bandit myBandit;
        int nextRandom = 0;

        public Wheel(Bandit insertedIn) 
        { 
            myBandit = insertedIn;
            // make shure the wheel isn't empty
            for (int i = 0; i < ShowsSymbols; i++)
            {
                Spin(false, false);
            }
        }

        /// <summary>
        /// Rotate the wheel one symbol
        /// </summary>
        /// <param name="interfere">Interfere with the outcome of the spin</param>
        /// <param name="decide">Decide what the wheel should show after the spin</param>
        public void Spin(bool interfere = true, bool decide = false)
        {
            var allowedSymbols = myBandit.Symbols;
            if (interfere) allowedSymbols = myBandit.GetAllowedSymbols();
            int symbol;
            if (decide)
            {
                symbol = myBandit.NextSymbol(this);
            }
            else
            {
                symbol = allowedSymbols[random.Next(allowedSymbols.Count)];
                nextRandom++;
                if (nextRandom >= 100000)
                {
                    random = new Random();
                }
            }

            RotateIn(symbol);
            myBandit.ForceSymbols(this);
        }

        /// <summary>
        /// Rotate the wheel once to display the provided symbol first in the wheel
        /// </summary>
        /// <param name="symbol">The symbol to add</param>
        public void RotateIn(int symbol)
        {
            Symbols.Insert(0, symbol);
            if (Symbols.Count > ShowsSymbols)
                Symbols.RemoveAt(Symbols.Count-1);
        }
    }
}
