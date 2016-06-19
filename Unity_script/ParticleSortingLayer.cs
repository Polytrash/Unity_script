using UnityEngine;
using System.Collections;

public class ParticleSortingLayer : MonoBehaviour {


    [SerializeField]
    private string _sortingLayerName = "Default";
	public int sortingOrder;

    // Use this for initialization
    void Start () {
		GetComponent<ParticleSystem>().GetComponent<Renderer>().sortingLayerName = _sortingLayerName;
		GetComponent<ParticleSystem>().GetComponent<Renderer>().sortingOrder = sortingOrder;
	}
}