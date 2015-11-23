using UnityEngine;
using System.Collections;

public class slider : MonoBehaviour {

	private float hSliderValue = 0;
	private AnimationState myAnimation;
	private bool sliderClick = false;
	
	 // Use this for initialization
	void Start () 
	{
		
	 	myAnimation = GetComponent<Animation>()["Take 001"];
    	myAnimation.speed=0;
		 
	}
	
	// Update is called once per frame
	void Update () 
	{
		
		//Assigns Slider value to animation time
		
    	myAnimation.time = hSliderValue;
		
		//Varaiable and conditional to assign boolean value to sliderClick
		
		sliderClick = false;
     
		if(Input.GetMouseButtonDown (0)== true || Input.GetMouseButtonDown (1)==true)
		{
			sliderClick = true;
		}
 
	}
	
	
	void OnGUI() 
 	{
		//Background for animation controls
		GUI.Box (new Rect (10,Screen.height-40, 360,40),(30 * myAnimation.time).ToString());
		
		// GUI.Box (new Rect (10, 20, 85, 25), "Period");
     
		//Uses animation speed check to show the either play or pause buttons    
		if (myAnimation.speed ==1)
		{
			if (GUI.Button (new Rect (15,Screen.height-30,50,20),"||")) //Pauses Animation
        	{
				myAnimation.speed=0.0f;
			}        
		}		
    	else
		{
			if (GUI.Button (new Rect (15, Screen.height-30,50,20),"➤")) //Plays animation
			{
				myAnimation.speed = 1;
         }
		}
		
		
		//A click on the slider area will pause the animation
        if (new Rect(70, Screen.height - 25, 275, 10).Contains(Event.current.mousePosition) && sliderClick == true)
		{
			myAnimation.speed = 0;    
		}
		
    	//click and drag slider to control animation playback
		hSliderValue = (GUI.HorizontalSlider (new Rect (70, Screen.height-25,275,10), myAnimation.time,0.0f,myAnimation.length));
		
		//Stop animation when it ends
		if(myAnimation.time >= 83.2)
   		{
			myAnimation.speed = 0;
		}
		
	}

}
