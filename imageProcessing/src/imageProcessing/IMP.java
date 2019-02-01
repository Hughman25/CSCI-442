/*
 *Hunter Lloyd & Matthew Sagen
 * Copyrite.......I wrote, ask permission if you want to use it outside of class. 
 */
package imageProcessing;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.File;
import java.awt.image.PixelGrabber;
import java.awt.image.MemoryImageSource;
import java.util.HashMap;
import java.util.prefs.Preferences;

class IMP implements MouseListener{
   JFrame frame;
   JPanel mp;
   JButton start;
   JScrollPane scroll;
   
   JMenuItem openItem, exitItem, resetItem;
   Toolkit toolkit;
   File pic;
   ImageIcon img;
   int colorX, colorY;
   int [] pixels;
   int [] results;
   private HashMap<Integer, Integer> redfreq = new HashMap<Integer,Integer>();
   private HashMap<Integer, Integer> greenfreq = new HashMap<Integer,Integer>();
   private HashMap<Integer, Integer> bluefreq = new HashMap<Integer,Integer>();
   private MyPanel redPanel = null;
   private MyPanel greenPanel = null;
   private MyPanel bluePanel = null;
   //Instance Fields you will be using below
   
   //This will be your height and width of your 2d array
   int height=0, width=0;
   
   //your 2D array of pixels
    int picture[][];
    int originalPic[][];

    /* 
     * In the Constructor I set up the GUI, the frame the menus. The open pulldown 
     * menu is how you will open an image to manipulate. 
     */
   IMP()
   {
      toolkit = Toolkit.getDefaultToolkit();
      frame = new JFrame("Image Processing Software by Hunter");
      JMenuBar bar = new JMenuBar();
      JMenu file = new JMenu("File");
      JMenu functions = getFunctions();
      frame.addWindowListener(new WindowAdapter(){
            @Override
              public void windowClosing(WindowEvent ev){quit();}
            });
      openItem = new JMenuItem("Open");
      openItem.addActionListener(new ActionListener(){
            @Override
          public void actionPerformed(ActionEvent evt){ handleOpen(); }
           });
      resetItem = new JMenuItem("Reset");
      resetItem.addActionListener(new ActionListener(){
            @Override
          public void actionPerformed(ActionEvent evt){ reset(); }
           });     
      exitItem = new JMenuItem("Exit");
      exitItem.addActionListener(new ActionListener(){
            @Override
          public void actionPerformed(ActionEvent evt){ quit(); }
           });
      file.add(openItem);
      file.add(resetItem);
      file.add(exitItem);
      bar.add(file);
      bar.add(functions);
      frame.setSize(600, 600);
      mp = new JPanel();
      mp.setBackground(new Color(0, 0, 0));
      scroll = new JScrollPane(mp);
      frame.getContentPane().add(scroll, BorderLayout.CENTER);
      JPanel butPanel = new JPanel();
      butPanel.setBackground(Color.black);
      start = new JButton("start");
      start.setEnabled(false);
      start.addActionListener(new ActionListener(){
            @Override
          public void actionPerformed(ActionEvent evt){ fun1(); }
           });
      butPanel.add(start);
      frame.getContentPane().add(butPanel, BorderLayout.SOUTH);
      frame.setJMenuBar(bar);
      frame.setVisible(true);      
   }
   
   /* 
    * This method creates the pulldown menu and sets up listeners to selection of the menu choices. If the listeners are activated they call the methods 
    * for handling the choice, fun1, fun2, fun3, fun4, etc. etc. 
    */
   
  private JMenu getFunctions(){
     JMenu fun = new JMenu("Functions");
     JMenuItem firstItem = new JMenuItem("MyExample - fun1 method");
     JMenuItem secondItem = new JMenuItem("Rotate Image: 90 Degrees");
     JMenuItem thirdItem = new JMenuItem("Gray Scale");
     JMenuItem fourthItem = new JMenuItem("Blur Image");
     JMenuItem fifthItem = new JMenuItem("5x5 mask");
     JMenuItem sixthItem = new JMenuItem("Show Histogram");
     JMenuItem seventhItem = new JMenuItem("Equalize Image");
     JMenuItem eigthItem = new JMenuItem("Track Object");
     
     firstItem.addActionListener(new ActionListener(){
            @Override
          public void actionPerformed(ActionEvent evt){fun1();}
           });
     secondItem.addActionListener(new ActionListener(){
         @Override
       public void actionPerformed(ActionEvent evt){rotate90();}
        });
     thirdItem.addActionListener(new ActionListener(){
         @Override
       public void actionPerformed(ActionEvent evt){grayScale();}
        });
     fourthItem.addActionListener(new ActionListener(){
         @Override
       public void actionPerformed(ActionEvent evt){blur();}
        });
     fifthItem.addActionListener(new ActionListener(){
         @Override
       public void actionPerformed(ActionEvent evt){mask();}
        });
     sixthItem.addActionListener(new ActionListener(){
         @Override
       public void actionPerformed(ActionEvent evt){showHistogram();}
        });
     seventhItem.addActionListener(new ActionListener(){
         @Override
       public void actionPerformed(ActionEvent evt){equalizeImage();}
        });
     eigthItem.addActionListener(new ActionListener(){
         @Override
       public void actionPerformed(ActionEvent evt){trackObject();}
        });
      fun.add(firstItem);
      fun.add(secondItem);
      fun.add(thirdItem);
      fun.add(fourthItem);
      fun.add(fifthItem);
      fun.add(sixthItem);
      fun.add(seventhItem);
      fun.add(eigthItem);

      return fun;   

  }
  
  /*
   * This method handles opening an image file, breaking down the picture to a one-dimensional array and then drawing the image on the frame. 
   * You don't need to worry about this method. 
   */
    private void handleOpen() {
    		img = new ImageIcon();
    		JFileChooser chooser = new JFileChooser();
    		Preferences pref = Preferences.userNodeForPackage(IMP.class);
    		String path = pref.get("DEFAULT_PATH", "");

    		chooser.setCurrentDirectory(new File(path));
    		int option = chooser.showOpenDialog(frame);
     
    		if(option == JFileChooser.APPROVE_OPTION) {
    			pic = chooser.getSelectedFile();
    			pref.put("DEFAULT_PATH", pic.getAbsolutePath());
    			img = new ImageIcon(pic.getPath());
    		}
    		width = img.getIconWidth();
	     height = img.getIconHeight(); 
	     JLabel label = new JLabel(img);
	     label.addMouseListener(this);
	     pixels = new int[width*height]; 
	     results = new int[width*height];       
	     Image image = img.getImage();
	        
	     PixelGrabber pg = new PixelGrabber(image, 0, 0, width, height, pixels, 0, width );
	     try{
	         pg.grabPixels();
	     }
	     catch(InterruptedException e){
	          System.err.println("Interrupted waiting for pixels");
	          return;
	     }
	     for(int i = 0; i<width*height; i++) {
	        results[i] = pixels[i];  
	     }
	     turnTwoDimensional();
	     mp.removeAll();
	     mp.add(label);
	     mp.revalidate();
	  }
	  
  /*
   * The libraries in Java give a one dimensional array of RGB values for an image, I thought a 2-Dimensional array would be more usefull to you
   * So this method changes the one dimensional array to a two-dimensional. 
   */
  private void turnTwoDimensional(){
     picture = new int[height][width];
     for(int i=0; i<height; i++)
       for(int j=0; j<width; j++)
          picture[i][j] = pixels[i*width+j];
     originalPic = picture;
  }
  /*
   *  This method takes the picture back to the original picture
   */
  private void reset(){
	  if(img != null) {//if there is an image previously selected, allow it to be reset.
		   JLabel label = new JLabel(img);
		   label.addMouseListener(this);
	       Image image = img.getImage();
	       PixelGrabber pg = new PixelGrabber(image, 0, 0, width, height, pixels, 0, width );
	       try{
	           pg.grabPixels();
	       }
	       catch(InterruptedException e){
	    	   		System.err.println("Interrupted waiting for pixels");
	            return;
	       }
	       for(int i = 0; i<width*height; i++) {
	          results[i] = pixels[i];  
	       }
	       turnTwoDimensional();
	       mp.removeAll();
	       mp.repaint();
	       mp.add(label);
	       mp.revalidate();
	  }
	  else {//handle if the user selects reset before importing an image
		  JOptionPane.showMessageDialog(mp, "Error: No picture selected. Open an image and Try again.");
	  }
    }
  /*
   * This method is called to redraw the screen with the new image. 
   */
  private void resetPicture(int height, int width, int[][] picture){
	  for(int i = 0; i < height; i++) {
		  for(int j = 0; j < width; j++) {
			  pixels[i*width+j] = picture[i][j];
		  }
      }
      Image img2 = toolkit.createImage(new MemoryImageSource(width, height, pixels, 0, width)); 
      JLabel label2 = new JLabel(new ImageIcon(img2));    
      mp.removeAll();
      mp.repaint();
      mp.add(label2);
      mp.revalidate(); 
  }
  /*
   * This method takes a single integer value and breaks it down doing bit manipulation to 4 individual int values for A, R, G, and B values
   */
  private int [] getPixelArray(int pixel){
      int temp[] = new int[4];
      temp[0] = (pixel >> 24) & 0xff;
      temp[1]   = (pixel >> 16) & 0xff;
      temp[2] = (pixel >>  8) & 0xff;
      temp[3]  = (pixel      ) & 0xff;
      return temp;
   }
   /*
    * This method takes an array of size 4 and combines the first 8 bits of each to create one integer. 
   */
  private int getPixels(int rgb[]){
         int alpha = 0;
         int rgba = (rgb[0] << 24) | (rgb[1] <<16) | (rgb[2] << 8) | rgb[3];
        return rgba;
  }
  
  public void getValue(){
      int pix = picture[colorY][colorX];
      int temp[] = getPixelArray(pix);
      System.out.println("Color value " + temp[0] + " " + temp[1] + " "+ temp[2] + " " + temp[3]);
    }
  
  /**************************************************************************************************
   * This is where you will put your methods. Every method below is called when the corresponding pulldown menu is 
   * used. As long as you have a picture open first the when your fun1, fun2, fun....etc method is called you will 
   * have a 2D array called picture that is holding each pixel from your picture. 
   *************************************************************************************************/
   /*
    * Example function that just removes all red values from the picture. 
    * Each pixel value in picture[i][j] holds an integer value. You need to send that pixel to getPixelArray the method which will return a 4 element array 
    * that holds A,R,G,B values. Ignore [0], that's the Alpha channel which is transparency, we won't be using that, but you can on your own.
    * getPixelArray will breaks down your single int to 4 ints so you can manipulate the values for each level of R, G, B. 
    * After you make changes and do your calculations to your pixel values the getPixels method will put the 4 values in your ARGB array back into a single
    * integer value so you can give it back to the program and display the new picture. 
    */
  private void fun1(){
    for(int i=0; i<height; i++){
    		for(int j=0; j<width; j++){
    	   		int rgbArray[] = new int[4];
    	   		//get three ints for R, G and B
    	   		rgbArray = getPixelArray(picture[i][j]);
    	   		rgbArray[1] = 0;
    	   		//take three ints for R, G, B and put them back into a single int
    	   		picture[i][j] = getPixels(rgbArray);
        } 
    }
    resetPicture(height, width, picture);
  }
  
  /*\
   * Method to rotate an image by 90 degrees
  \*/
  private void rotate90() {
	  //get all of the original pixels
	  //rotate them around the center pixel 90 degrees.
	 
	  int[][] rotatedPicture = new int[width][height];
	  for(int i = 0; i < height; i++) {
		  for(int j = 0; j < width; j++){   
			  int rgbArray[] = new int[4];
			  //get three ints for R, G and B
			  rgbArray = getPixelArray(picture[i][j]);
			  rotatedPicture[j][i] = getPixels(rgbArray);
		  } 
	  }
	  resetPicture(width, height, rotatedPicture);
  }
  
  private void grayScale() {
	  for(int i = 0; i < height; i++) {
		  for(int j = 0; j < width; j++){   
			  int rgbArray[] = new int[4];
			  //get four ints for A, R, G and B
			  rgbArray = getPixelArray(picture[i][j]);
			  // luminosity function 0.21 R + 0.72 G + 0.07 B
			  rgbArray[0] = 255;
			  rgbArray[1] = (int) ((rgbArray[1] * 0.21) + (rgbArray[2] * 0.72) + (rgbArray[3] * 0.07));//red
			  rgbArray[2] = (int) ((rgbArray[1] * 0.21) + (rgbArray[2] * 0.72) + (rgbArray[3] * 0.07));//green
			  rgbArray[3] = (int) ((rgbArray[1] * 0.21) + (rgbArray[2] * 0.72) + (rgbArray[3] * 0.07));//blue
	  	   	  //take three ints for R, G, B and put them back into a single int
	  	   	  picture[i][j] = getPixels(rgbArray);
		  } 
	  }
	  resetPicture(height,width,picture);
  }
  
  private void blur() {
	  int[][] picture2 = picture;
	  int rgbArray[] = new int[4];
	  //5x5 blur
	  for(int i = 2; i < height - 2; i++) {
		  for(int j = 2; j < width - 2; j++){   
			  
			  //get four integers for A, R, G and B from surrounding pixels
			  //top row
			  int[] top0 = getPixelArray(picture[i-2][j-2]);
			  int[] top1 = getPixelArray(picture[i-2][j-1]);
			  int[] top2 = getPixelArray(picture[i-2][j]);
			  int[] top3 = getPixelArray(picture[i-2][j+1]);
			  int[] top4 = getPixelArray(picture[i-2][j+2]);
			  
			  //left column between top row and bottom row
			  int[] row1L = getPixelArray(picture[i-1][j-2]);
			  int[] row2L = getPixelArray(picture[i][j-2]);
			  int[] row3L = getPixelArray(picture[i+1][j-2]);
			  
			  //right column between top row and bottom row
			  int[] row1R = getPixelArray(picture[i-1][j+2]);
			  int[] row2R = getPixelArray(picture[i][j+2]);
			  int[] row3R = getPixelArray(picture[i+1][j+2]);
			  
			  //bottom row
			  int[] bottom0 = getPixelArray(picture[i+2][j-2]);
			  int[] bottom1 = getPixelArray(picture[i+2][j-1]);
			  int[] bottom2 = getPixelArray(picture[i+2][j]);
			  int[] bottom3 = getPixelArray(picture[i+2][j+1]);
			  int[] bottom4 = getPixelArray(picture[i+2][j+2]);
			  
			  
			  int redAverage = (int)(top0[1] + top1[1] + top2[1] + top3[1] + top4[1] + row1L[1] + row2L[1] + row3L[1]
					         + row1R[1] + row2R[1] + row3R[1] + bottom0[1] + bottom1[1] + bottom2[1] + bottom3[1] + bottom4[1]) / 16;
			  
			  int greenAverage = (int)(top0[2] + top1[2] + top2[2] + top3[2] + top4[2] + row1L[2] + row2L[2] + row3L[2]
				         + row1R[2] + row2R[2] + row3R[2] + bottom0[2] + bottom1[2] + bottom2[2] + bottom3[2] + bottom4[2]) / 16;
			  
			  int blueAverage = (int)(top0[3] + top1[3] + top2[3] + top3[3] + top4[3] + row1L[3] + row2L[3] + row3L[3]
				         + row1R[3] + row2R[3] + row3R[3] + bottom0[3] + bottom1[3] + bottom2[3] + bottom3[3] + bottom4[3]) / 16;
			  
	  	   	  //take three ints for R, G, B and put them back into a single int
			  rgbArray[0] = 255; //set Alpha to 255 for every iteration
			  rgbArray[1] = redAverage;
			  rgbArray[2] = greenAverage;
			  rgbArray[3] = blueAverage;
			  picture2[i][j] = getPixels(rgbArray);
		  }
	  }
	  //set the picture equal to the blurred image
	  picture = picture2;
	  resetPicture(height,width,picture);
  }
  private void mask() {
	  grayScale();
	  int[][] picture2 = picture;
	  int rgbArray[] = new int[4];
	  int[][] mask = {{-1,-1,-1,-1,-1},
				      {-1, 0, 0, 0,-1},
				      {-1, 0, 10, 0,-1},
				      {-1, 0, 0, 0,-1},
				      {-1,-1,-1,-1,-1}};
	  
	  for(int i = 2; i < height - 2; i++) {
		  for(int j = 2; j < width - 2; j++) {
			  //get four integers for A, R, G and B from surrounding pixels
			  //top row
			  int[] center = getPixelArray(picture[i][j]);
			  int n = 0;
			  int total = 0;
			  for(int z = -2; z < 2; z++) {
				  int m = 0;
				  total += getPixelArray(picture[i+z][j-2])[1] * mask[n][m++];
				  total += getPixelArray(picture[i+z][j-1])[1] * mask[n][m++];
				  total += getPixelArray(picture[i+z][j])[1] * mask[n][m++];
				  total += getPixelArray(picture[i+z][j+1])[1] * mask[n][m++];
				  total += getPixelArray(picture[i+z][j+2])[1] * mask[n][m++];
				  n++;
			  }
			  if(total > 500) {
				  rgbArray[0] = 0;
				  rgbArray[1] = 0;
				  rgbArray[2] = 0;
				  rgbArray[3] = 0;
			  }
			  else if (total < -500){
				  rgbArray[0] = 255;
				  rgbArray[1] = 255;
				  rgbArray[2] = 255;
				  rgbArray[3] = 255;
			  }
			  else {
				  for(int k = 1; k < rgbArray.length; k++) {
					  rgbArray[k] = total;
					  
				  }
			  }
			  picture2[i][j] = getPixels(rgbArray);
			  
		  }
	  }
	
	  resetPicture(height,width,picture2);
  }
  private void showHistogram() {
	  int rgbArray[] = new int[4];
	  //map: (0-255, frequency)
	  //initialize all frequencies to 0
	  for(int i = 0; i <= 255; i++) {
		  redfreq.put(i,0);
		  greenfreq.put(i,0);
		  bluefreq.put(i,0);
	  }
	  //loop through picture and map the frequencies of each RGB value of each pixel.
	  for(int i = 0; i < height; i++) {
		  for(int j = 0; j < width; j++) {
			  rgbArray = getPixelArray(picture[i][j]);			 
			  redfreq.put(rgbArray[1], redfreq.get(rgbArray[1]) + 1);
			  greenfreq.put(rgbArray[2], greenfreq.get(rgbArray[2]) + 1);
			  bluefreq.put(rgbArray[3], bluefreq.get(rgbArray[3]) + 1);
		  }
	  }
	  //set up panels to show the histograms
	  redPanel   = new MyPanel("red", redfreq);
	  greenPanel = new MyPanel("green", greenfreq);
	  bluePanel  = new MyPanel("blue", bluefreq);
	  redPanel.drawHistogram(start, redPanel);
	  greenPanel.drawHistogram(start, greenPanel);
	  bluePanel.drawHistogram(start, bluePanel);
  }
  private void equalizeImage() {
	  /*
	   * Original Red Value " + rgbArray[1]
		 The accumultive frequency at this pixel " + r + ", " + c + " is " + red[rgbArray[1]]
		 Total # of Pixels " + (width*height)
		 Do the math
		 round(frequency / total pixels) * max pixel value(255)"
		 New red value " + Math.round(((float)red[rgbArray[1]]/(float)(width*height))*255.0)
		 To calculate the frequency
		 ++red[rgbArray[1]];
	  */
	  //only allow equalization if the histogram has been displayed
	  if(redPanel != null && greenPanel != null && bluePanel !=null) {
		  double totalPixels = width * height;
		  int[] rgbArray = new int[4];
		  double cR = 0;
		  double cG = 0;
		  double cB = 0;
		  double[] cuR = new double[256];
		  double[] cuG = new double[256];
		  double[] cuB = new double[256];
		  
		  for(int i = 0; i < 256; i++) {
			  cR += redfreq.get(i);
			  cG += greenfreq.get(i);
			  cB += bluefreq.get(i);
			  cuR[i] = (cR/totalPixels)*255;
			  cuG[i] = (cG/totalPixels)*255;
			  cuB[i] = (cB/totalPixels)*255;
			  
		  }
		  //get the minimum value from the table
		  //map: (0-255, frequency)
		  for(int i = 0; i < height; i++) {
			  for(int j = 0; j < width; j++) {
				 rgbArray = getPixelArray(picture[i][j]);
				 
				 rgbArray[0]  = 255;
				 rgbArray[1]  = (int) cuR[rgbArray[1]];
				 rgbArray[2]  = (int) cuG[rgbArray[2]];
				 rgbArray[3]  = (int) cuB[rgbArray[3]];
				 picture[i][j] = getPixels(rgbArray);
			  }
		  }
		  resetPicture(height,width,picture);
	  }
	  else {
		  JOptionPane.showMessageDialog(mp, "Error: Must display histogram before choosing this option.");
	  }
	  
  }
  private void trackObject() {
	  int[] rgbArray = new int[4];

	  for(int i = 0; i < height; i++) {
		  for(int j = 0; j < width; j++) {
				 rgbArray = getPixelArray(picture[i][j]);
				 if((rgbArray[1] < 255 && rgbArray[1] > 235) && 
					(rgbArray[2] < 255 && rgbArray[2] > 155) && 
					(rgbArray[3] < 255 && rgbArray[3] > 0)) {
					 
					 rgbArray[0] = 255;
					 rgbArray[1] = 255;
					 rgbArray[2] = 255;
					 rgbArray[3] = 255;
					 
				 }
				 else {
					 rgbArray[0] = 255;
					 rgbArray[1] = 0;
					 rgbArray[2] = 0;
					 rgbArray[3] = 0;
				 }
				 picture[i][j] = getPixels(rgbArray);
		  }
	  }
	  resetPicture(height,width,picture);
  }
  private void quit(){  
     System.exit(0);
  }

    @Override
   public void mouseEntered(MouseEvent m){}
    @Override
   public void mouseExited(MouseEvent m){}
    @Override
   public void mouseClicked(MouseEvent m){
        colorX = m.getX();
        colorY = m.getY();
        System.out.println(colorX + "  " + colorY);
        getValue();
        start.setEnabled(true);
    }
    @Override
   public void mousePressed(MouseEvent m){}
    @Override
   public void mouseReleased(MouseEvent m){}
   
   public static void main(String [] args){
      IMP imp = new IMP();
   }
}