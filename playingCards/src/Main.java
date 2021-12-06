public class Main {

    public static void main(String[] args){

        String[] suitVal = {"Spades", "Hearts", "Diamonds", "Clubs"};
        String[] setVal = { "2", "3", "4", "5","6", "7","8","9","10","Jack","Queen","King","Ace"};
        deck deckOfCards[]=new deck[52];
        int cardCount = -1;

        for(int i=0;i<4;i++){
            for(int j=0;j<13;j++){
                cardCount++;
                deckOfCards[cardCount] = new deck(suitVal[i],setVal[j]);
            }
        }
        deckOfCards[0].cardSelect();
        deckOfCards[13].cardSelect();
        deckOfCards[26].cardSelect();
        deck.shuffle(deckOfCards);
        deckOfCards[0].cardSelect();
        deckOfCards[13].cardSelect();
        deckOfCards[26].cardSelect();
    }
}
