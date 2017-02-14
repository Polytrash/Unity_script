using UnityEngine;
using System.Collections;

[ExecuteInEditMode]
public class showNormal : MonoBehaviour {

    // Use this for initialization
    private Mesh mesh;
    public float normalLength = 0.0001f;

    // Use this for initialization
    void Start()
    {
        mesh = GetComponent<MeshFilter>().sharedMesh;
    }
    // Update is called once per frame
    void Update()
    {
        for (int i = 0; i < mesh.vertices.Length; i++)
        {
            Vector3 norm = transform.TransformDirection(mesh.normals[i]);
            Vector3 vert = transform.TransformPoint(mesh.vertices[i]);
            Debug.DrawRay(vert, norm /10f , Color.red);
        }
    }
}
