using System.Linq.Expressions;

namespace OneArmedBandit
{
    public abstract class Bandit
    {
        /// <summary>
        /// Name of the one armed bandit
        /// </summary>
        public abstract string Name { get; set; }

        /// <summary>
        /// Contains ids for the things that go on the wheels
        /// </summary>
        public abstract List<int> Symbols { get; set; }

        /// <summary>
        /// The wheels that display the outcome of the bet
        /// </summary>
        public abstract List<Wheel> Wheels { get; set; }

        /// <summary>
        /// Number of lines being played
        /// </summary>
        public abstract int Lines { get; set; }

        /// <summary>
        /// Number of lines that are available
        /// </summary>
        public abstract int LinesAvailable { get; }

        /// <summary>
        /// The ammount to bet on each line
        /// </summary>
        public abstract int BetPerLine { get; set; }

        /// <summary>
        /// The current amount of money in the bandit
        /// </summary>
        public abstract int CurrentBalance { get; }

        /// <summary>
        /// Add to the current balance
        /// </summary>
        /// <param name="ammount">The amount to add</param>
        public abstract void InsertCoins(int ammount);

        /// <summary>
        /// Cash out the current balance
        /// </summary>
        /// <returns>The current balance</returns>
        public abstract int CashOut();

        /// <summary>
        /// Pull the lever to bet
        /// </summary>
        public abstract void Pull();

        /// <summary>
        /// Increment the roll of the wheels
        /// </summary>
        public abstract void Roll();

        /// <summary>
        /// End the rolling of the wheels
        /// </summary>
        /// <returns>The ammount won</returns>
        public abstract int EndRoll();

        /// <summary>
        /// When interfering with the outcome of a wheelspin this method is called by the wheel to determine which symbols its allowed to land on
        /// </summary>
        /// <returns>The acceptable set of outcomes for the spin</returns>
        public abstract List<int> GetAllowedSymbols();

        /// <summary>
        /// When interfering with th outcome of a wheelspin this method is called after the spin to allow the slot machine to change any symbols
        /// </summary>
        /// <param name="wheel">The wheel that has been spun</param>
        public abstract void ForceSymbols(Wheel wheel);

        /// <summary>
        /// Provide the a symbol for the wheel to put into the combination it lands on
        /// </summary>
        /// <param name="wheel"></param>
        /// <returns></returns>
        public abstract int NextSymbol(Wheel wheel);



    }
}