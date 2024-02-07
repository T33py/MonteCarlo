using System.Numerics;

namespace BlackJack
{
    public class Game
    {
        Random random = new Random();
        int didx = 0;
        List<Card> deck = new List<Card>();
        Dealer dealer = new Dealer();
        public int BlackjackPayoutRatioHi = 3; // this would be the 3 in a 3/2 payout
        public int BlackjackPayoutRatioLo = 2; // this would be the 2 in a 3/2 payout
        public List<IPlayer> Players = new List<IPlayer>();


        public Game()
        {
            Setup(1);
        }

        public Game(int decks)
        {
            Setup(decks);
        }

        public void PlayRound()
        {
            ClearHands();
            DealHands();
            PlayersPlay();
            DealerPlays();
            DoResults();
        }

        void PlayersPlay()
        {
            foreach (IPlayer p in Players)
            {
                if (p.Hands.Count == 0)
                    continue;

                var playingHand = 0;
                while (PlayerPlaying(p))
                {
                    DoPlayerHand(p.Hands[playingHand], p);
                    playingHand = (playingHand + 1) % p.Hands.Count;
                }
            }
        }

        void DoPlayerHand(Hand hand, IPlayer player)
        {
            while (hand.CurrentState == Hand.State.Playing)
            {
                if (hand.Cards.Count == 2 && hand.Value == 21)
                {
                    hand.CurrentState = Hand.State.BlackJack;
                    continue;
                }
                if (hand.CanSplit() && player.Split(hand, dealer.Shows))
                {
                    var newHand = new Hand();
                    newHand.Bet = hand.Bet;
                    var card = hand.Cards[1];
                    player.Hands.Add(newHand);
                    hand.Cards.Remove(card);
                    newHand.Cards.Add(card);
                    hand.Cards.Add(NextCard(false));
                    newHand.Cards.Add(NextCard(false));
                }
                else if (hand.CanDouble() && player.DoubleDown(hand, dealer.Shows))
                {
                    hand.doubled = true;
                    hand.Cards.Add(NextCard(false));
                    hand.CurrentState = Hand.State.Stands;
                }
                else if (player.Hit(hand, dealer.Shows))
                {
                    hand.Cards.Add(NextCard(false));
                }
                else
                {
                    hand.CurrentState = Hand.State.Stands;
                }

                if (hand.Value > 21)
                {
                    hand.CurrentState = Hand.State.Bust;
                }
            }
        }

        void DoResults()
        {
            foreach(var player in Players)
            {
                DoResult(player);
            }
            DoResult(dealer.Hand);
            if (deck.Count - (didx + 1) < Players.Count * 4)
            {
                Shuffle(deck);
            }
        }

        void DoResult(IPlayer player)
        {
            int payout = 0;
            foreach (var hand in player.Hands)
            {
                payout += DoResult(hand);
            }
            player.Money += payout;
            player.Result(dealer.Hand, payout);
        }

        int DoResult(Hand hand)
        {
            int payout = 0;
            if (hand.CurrentState == Hand.State.BlackJack)
            {
                payout += (hand.Bet / BlackjackPayoutRatioLo) * BlackjackPayoutRatioHi;
            }
            else if (hand.CurrentState == Hand.State.Bust) 
            {
                payout -= hand.Bet;
                if (hand.doubled)
                    payout -= hand.Bet;
            }
            else if (hand.Value > dealer.Hand.Value)
            {
                hand.CurrentState = Hand.State.Won;
                payout += hand.Bet;
                if (hand.doubled)
                    payout += hand.Bet;
            }
            else if (dealer.Hand.Value > 21)
            {
                hand.CurrentState = Hand.State.Won;
                payout += hand.Bet;
                if (hand.doubled)
                    payout += hand.Bet;
            }
            else if (hand.Value == dealer.Hand.Value)
            {
                hand.CurrentState = Hand.State.Push;
            }
            else
            {
                hand.CurrentState = Hand.State.Lost;
                payout -= hand.Bet;
                if (hand.doubled)
                    payout -= hand.Bet;
            }
            return payout;
        }

        bool PlayerPlaying(IPlayer player)
        {
            foreach(Hand hand in player.Hands)
            {
                if (hand.CurrentState == Hand.State.Playing)
                    return true;
            }
            return false;
        }

        void DealerPlays()
        {
            while (dealer.Hit())
            {
                dealer.Hand.Cards.Add(NextCard(false));
            }
        }

        void DealHands()
        {
            var hands = new List<Hand>();
            // setup number of hands for each player
            foreach (var player in Players)
            {
                var bets = player.PlayHands();
                for (int i = 0; i < bets; i++)
                {
                    var hand = new Hand();
                    hand.Bet = player.Bet();
                    player.Hands.Add(hand);
                    hands.Add(hand);
                }
            }
            // deal first card
            foreach(var hand in hands)
            {
                hand.Cards.Add(NextCard(false));
            }
            dealer.Hand.Cards.Add(NextCard(true));
            // deal second card
            foreach (var hand in hands)
            {
                hand.Cards.Add(NextCard(false));
            }
            dealer.Hand.Cards.Add(NextCard(false));

        }

        Card NextCard(bool faceDown)
        {
            var card = deck[didx];
            didx = (didx + 1) % deck.Count;
            if (didx == 0)
                Shuffle(deck);

            foreach(var p in Players)
            {
                p.OnCardDealt(card, faceDown);
            }
            return card;
        }

        void ClearHands()
        {
            dealer.Hand.Cards.Clear();
            foreach(IPlayer p in Players)
            {
                p.Hands.Clear();
            }
        }

        void Setup(int decks)
        {
            SetupDeck();
            for (int i = 1; i < decks; i++)
            {
                var cp = new List<Card>();
                foreach(var card in deck)
                {
                    cp.Add(card);
                }
                deck.AddRange(cp);
            }

            Shuffle(deck);
        }

        void SetupDeck()
        {
            foreach (var symbol in Card.Symbols)
            {
                foreach (var suit in Card.Suits)
                {
                    deck.Add(new Card(symbol, suit));
                }
            }
        }

        void Shuffle(List<Card> deck)
        {
            random = new Random(((int)DateTime.Now.Ticks));
            var shuffled = new List<Card>();
            while (deck.Count > 0)
            {
                var card = deck[random.Next(deck.Count)];
                shuffled.Add(card);
                deck.Remove(card);
            }
            foreach (var card in shuffled)
            {
                deck.Add(card);
            }

            foreach(var p in Players)
            {
                p.OnShuffle();
            }
        }

        public void AddPlayer(IPlayer player)
        {
            Players.Add(player);
            Console.WriteLine($"{player.Name} plays");
        }
    }
}