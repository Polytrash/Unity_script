using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public class Effect : MonoBehaviour {

	public float hSliderValue = 0.0F;


	void OnGUI(){

		GUI.Button (new Rect (480, 10, 100, 30), "Save");
		GUI.Button (new Rect (480, 50, 100, 30), "Load");
		hSliderValue = GUI.HorizontalSlider(new Rect(480, 120, 200, 30), hSliderValue, 0.0F, 10.0F);
		// ラベルにhSliderValueの値を表示する
		GUI.Label(new Rect(400, 170, 200, 20), "Animation Frame: " + hSliderValue);
	}



	// Shriken Particle 
	public bool[] shrikenParticle;

	public float  duration;

	public bool   looping;
	public bool   prewarm;

	public float  startDelay;
	public float  startLifetime;
	public float  startSpeed;
	public float  startSize;
	public float  startRotation;
	public Color  startColor;

	public float  gravityModifier;
	public float  inheritVelocity;
	public float  simulationSpace;
	public bool   playOnAwake;
	public int    maxParticles;

	// Emission 
	public bool[] emission;

	public bool   emissionP;
	public int    emissionRate;
	public float  burstTime;
	public int    particles;

	// Shape 
	public bool[] shape;

	public bool    shapeP;
	public float   angle;
	public float   radius;
	public int     emitFrom;
	public bool    randomDirection;

	// Velocity over Lifetime 
	public bool[] velocityOverLifetime;

	public Vector3 velocityOverLifetimeP;
	//public int space;

	// Limit Velocity over Lifetime
	public bool[] limitVelocityOverLifetime;

	public bool    separateAxis;
	public float   speed;
	public float   dampenLVOL;

	// Force over Lifetime
	public bool[] lifeTime;

	public Color   colorCOL;
	public int     space;
	public bool    randomize;


	// Color by Speed
	public bool[] colorBySpeed;

	public Color   colorCBS;
	public float[] speedRangeCBS;

	// Size over Lifetime

	public AnimationClip sizeSOL;

	// Size by Speed
	public bool[] sizeBySpeed;

	public AnimationClip sizeSBS;
	public float[] speedRangeSBS;

	// External Forces
	public bool[] externalForces;

	public float   multiplier;

	// Collision 
	public bool[] collision;

	public int     planes;
	public int     visualization;
	public float   dampenC;
	public float   bounce;
	public float   lifetimeLoss;
	public float   minKillSpeed;
	public float   particleRadius;
	public bool    sendCollisionMessage;

	// Texture Sheet Animation
	public bool[] textureSheetAnimation;

	public int[]   tiles;
	public int     animation;
	public AnimationClip frameOverTime;
	public int     cycles;

	// Renderer
	public bool[] renderer;

	public int 	   renderMode;
	public float   normalDirection;
	public Material material;
	public int     sortMode;
	public float   sortingFudge;
	public int     castShadews;
	public bool    receiveShadows;
	public float   maxParticleSize;
	public int     sortingLayer;
	public int     orderInLayer;
	public int     reflectionProbes;
	public GameObject anchorOverride;



}