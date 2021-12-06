public class deck {
    String suit;
    String set;

    public deck(String suitV, String setV){
        this.suit=suitV;
        this.set=setV;
    }

    public void cardSelect() {
        System.out.println("This card is the "+set+" of "+suit);
    }

    public static deck[] shuffle(deck[] deckVal){
        for(int i=0;i<52;i++) {
            int idCaller1 = (int) (Math.random() * 52);
            int idCaller2 = (int) (Math.random() * 52);
            deck placeHolder = deckVal[idCaller1];
            deckVal[idCaller1] = deckVal[idCaller2];
            deckVal[idCaller2] = placeHolder;
        }
        return deckVal;
    }

}
