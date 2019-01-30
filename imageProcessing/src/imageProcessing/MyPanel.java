package imageProcessing;
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.image.BufferedImage;
import java.util.HashMap;

public class MyPanel extends JPanel{
 
int startX, flag, startY, endX, endY;

    BufferedImage grid;
    Graphics2D gc;
    String color;
    HashMap<Integer,Integer> freq;
   

	public MyPanel(String color, HashMap<Integer, Integer> freq){
		   startX = startY = 0;
           endX = endY = 100;
           this.color = color;
           this.freq = freq;
 	}
	
    public void clear(){
       grid = null;
       repaint();
    }
    public void drawHistogram(JButton start, MyPanel panel) {
    	  JFrame frame = new JFrame(color);
    	  frame.setSize(350, 600);
    	  
    	  if(color == "red") {
        	  frame.setLocation(200, 0);
    	  }
    	  else if(color == "green") {
        	  frame.setLocation(510, 0);
    	  }
    	  else{
        	  frame.setLocation(820, 0);
    	  }
    	  
    	  frame.getContentPane().add(panel, BorderLayout.CENTER);
    	  frame.setVisible(true);
    	  start.setEnabled(true);
    }
    public void paintComponent(Graphics g){  
         super.paintComponent(g);
         Graphics2D g2 = (Graphics2D)g;
         if(grid == null){
            int w = this.getWidth();
            int h = this.getHeight();
            grid = (BufferedImage)(this.createImage(w,h));
            gc = grid.createGraphics();
            gc.drawLine(25, 400, 25, 0);
            gc.drawLine(25, 400, 280, 400);
           // gc.drawOval(23, 405, 8, 10);
            char[] bounds = {'0','2','5','5'};
            String zero = "0";
            String end = "255";
            
            gc.drawString(zero, 23, 415);
            gc.drawString(end, 265, 415);
            //loop through the hashmap and plot the frequency of each intensity.
            for(int i = 0; i < freq.size(); i++) {
            		gc.drawLine(i+25, 400, i+25, 400-(freq.get(i)/5));
            }

         }
         g2.drawImage(grid, null, 0, 0);
     }
    public void drawing(){ 
        gc.drawLine(startX, startY, endX, endY);
        repaint();
    }
}
