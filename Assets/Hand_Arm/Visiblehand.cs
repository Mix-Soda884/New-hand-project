using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Leap;
using Leap.Unity;
using UnityEngine.UI;

public class Visiblehand : MonoBehaviour
{
    [SerializeField]
    GameObject m_ProviderObject;
    public Text scoreText;
    Vector3 r1;
    Vector3 r0;
    public float r;
    
    LeapServiceProvider m_Provider;
    // Start is called before the first frame update
    void Start()
    {
        m_Provider = m_ProviderObject.GetComponent<LeapServiceProvider>();
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        Frame frame = m_Provider.CurrentFrame;

        // 右手と左手を取得する
        Hand rightHand = null;
        Hand leftHand = null;
        foreach (Hand hand in frame.Hands)
        {
            if (hand.IsRight)
            {
                rightHand = hand;
            }
            if (hand.IsLeft)
            {
                leftHand = hand;
            }
        }

        if (rightHand != null)
        {
            r0 = rightHand.Fingers[0].TipPosition;
            r1 = rightHand.Fingers[1].TipPosition;
            r = Vector3.Distance(r1, r0);

            //Debug.Log(rightHand.Fingers[0].TipPosition);
        }
    }
}