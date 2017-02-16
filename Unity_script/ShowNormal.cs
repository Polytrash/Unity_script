using UnityEngine;
using System.Collections;

[ExecuteInEditMode]
public class ShowNormal : MonoBehaviour {

    public Mesh mesh;
    public float normalLength = 0.1f;
    public bool isRed;


    void Start()
    {
        mesh = GetComponent<MeshFilter>().sharedMesh;
    }

    void Update()
    {
        Color col = Color.green;

        if (isRed) { col = Color.red; };

        mesh = GetComponent<MeshFilter>().sharedMesh;
        for (int i = 0; i < mesh.vertices.Length; i++)
        {
            Vector3 norm = transform.TransformDirection(mesh.normals[i]);
            Vector3 vert = transform.TransformPoint(mesh.vertices[i]);
            Debug.DrawRay(vert, norm * normalLength , col);
        }
    }
}
