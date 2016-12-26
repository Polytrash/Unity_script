using UnityEngine;
using System.Collections;

public class Sea_UVscroll : MonoBehaviour
{

    [SerializeField]
    private float scrollSpeedX = 1.0f;

    [SerializeField]
    private float scrollSpeedY = 1.0f;

    void Start()
    {
        GetComponent<Renderer>().sharedMaterial.SetTextureOffset("_FoamTex", Vector2.zero);
        GetComponent<Renderer>().sharedMaterial.SetFloat("_FoamRipple", 0);
        GetComponent<Renderer>().sharedMaterial.SetFloat("_WetAmount", 0);
    }

    void Update()
    {
        var x = Mathf.Repeat(Time.time * scrollSpeedX, 1);
        var y = Mathf.Repeat(Time.time * scrollSpeedY, 1);

        var offset = new Vector2(x, y);

        GetComponent<Renderer>().sharedMaterial.SetTextureOffset("_FoamTex", offset);
        GetComponent<Renderer>().sharedMaterial.SetFloat("_FoamRipple", Mathf.Abs( Mathf.Sin(Time.time * .5f)));
        GetComponent<Renderer>().sharedMaterial.SetFloat("_WetAmount", Mathf.Abs(Mathf.Sin(Time.time * .5f)));
    }
}