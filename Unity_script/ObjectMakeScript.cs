﻿using UnityEngine;
using System.Collections;

public class ObjectMakeScript : MonoBehaviour {

    public GameObject obj;
    public Vector3 spawnPoint;

    public void BuildObject()
    {
        Instantiate(obj, spawnPoint, Quaternion.identity);
    }

}