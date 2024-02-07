using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BlackJack
{
    public class Dealer
    {
        public Hand Hand { get; set; } = new Hand();

        // the dealer should be showing the 2nd card given
        public Card Shows { get => Hand.Cards[1]; }

        public bool Hit()
        {
            if (Hand.Value <= 16)
                return true;
            return false;
        }
    }
}
