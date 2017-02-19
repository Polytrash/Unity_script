using UnityEngine;
using System.Collections;

[ExecuteInEditMode]
public class ShowNormal : MonoBehaviour {
    private Mesh mesh;
    private SkinnedMeshRenderer skinMesh;
    private bool isMesh = true;
    public float normalLength = 0.1f;
    public bool isRed;


    void Start()
    {
        skinMesh = GetComponent<SkinnedMeshRenderer>();
        mesh = GetComponent<MeshFilter>().sharedMesh;
    }

    void Update()
    {
        Color col = Color.green;
        if (isRed) { col = Color.red; };
  
            try
            {
                mesh = GetComponent<MeshFilter>().sharedMesh;

                for (int i = 0; i < mesh.vertices.Length; i++)
                {
                    Vector3 norm = transform.TransformDirection(mesh.normals[i]);
                    Vector3 vert = transform.TransformPoint(mesh.vertices[i]);
                    Debug.DrawRay(vert, norm * normalLength, col,  0.0f, true);
                }
                 isMesh = true;
            }
            catch (MissingComponentException e)
            {
                Debug.Log("Show Normal disabled.");
            }


        if (!isMesh)
        {
            try
            {
                skinMesh = GetComponent<SkinnedMeshRenderer>();

                for (int i = 0; i < skinMesh.sharedMesh.vertices.Length; i++)
                {
                    Vector3 norm = skinMesh.sharedMesh.normals[i];
                    Vector3 vert = skinMesh.sharedMesh.vertices[i];
                    Debug.DrawRay(vert, norm * normalLength, col, 0.0f, true);
                }

            }
            catch (MissingComponentException e)
            {
                Debug.Log("Show Normal disabled.");
            }
        }   
    }
}
