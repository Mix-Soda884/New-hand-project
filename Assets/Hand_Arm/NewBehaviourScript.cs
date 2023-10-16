using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Text;
using Leap;
using Leap.Unity;
using UnityEngine.UIElements;

public class NewBehaviourScript : MonoBehaviour
{
    [SerializeField]
    //SerialHandler.cのクラス
    public SerialHandler serialHandler;
    public LeapServiceProvider m_Provider;
    GameObject m_ProviderObject;

    Vector3 right_normal;
    Vector3 right_direction;
    Vector3 right_position;
    private Transform emptyObjectTransform;
    Vector3 r1;
    Vector3 r0;
    float x;
    float ay;
    float zy;
    float zeroY;
    int q = 90;
    int w = 93;
    int e = 90;
    int r = 90;
    int t = 65;

    public VisibleBallHand handScript;
    public Visiblehand Visiblehand;


    void three_function(string a, int b, int c)
    {
        string p1;
        p1 = "{'start':" + $"[{a},{b},{c}]" + "}\n";
        print(p1);
        byte[] p1EncodedBytes = Encoding.GetEncoding("gbk").GetBytes(p1);
        string p1EncodedString = Encoding.GetEncoding("gbk").GetString(p1EncodedBytes);
        serialHandler.Write(p1EncodedString);
        Debug.Log(p1EncodedString);
        //ser.write("{'start':['pinmode',13,0]}\n".encode("gbk"))
    }
    void resetposition()
    {
        three_function("'servo_attach'", 0, 9);
        three_function("'servo_attach'", 1, 6);
        three_function("'servo_attach'", 2, 5);
        three_function("'servo_attach'", 3, 3);
        three_function("'servo_attach'", 4, 11);

        three_function("'servo_write'", 0, q);
        three_function("'servo_write'", 1, w);
        three_function("'servo_write'", 2, e);
        three_function("'servo_write'", 3, r);
        three_function("'servo_write'", 4, t);
    }
    void Start()
    {
        Invoke("resetposition", 3.0f);
        if (m_ProviderObject != null)
        {
            m_Provider = m_ProviderObject.GetComponent<LeapServiceProvider>();
        }
        else
        {
            Debug.LogError("m_ProviderObject is not assigned in the Inspector.");
        }
    }

    void FixedUpdate() //ここは0.001秒ごとに実行される
    {
        Frame frame = m_Provider.CurrentFrame;

        Hand rightHand = null;

        foreach (Hand hand in frame.Hands)
        {
            if (hand.IsRight)
            {
                rightHand = hand; // 右手情報を代入
                break; // 右手が見つかったらループを抜ける
            }
        }

        if (rightHand != null)
        {
            r0 = rightHand.Fingers[0].TipPosition;
            r1 = rightHand.Fingers[1].TipPosition;
            x = Vector3.Distance(r1, r0);
            x = x*13;

            right_normal = rightHand.PalmNormal;
            right_direction = rightHand.Direction;
            right_position = rightHand.PalmPosition;

            emptyObjectTransform = GameObject.Find("Leap motion Controller").transform;
            Vector3 zero_position = emptyObjectTransform.position;
            Vector3 zeroY_Zposition = new Vector3(right_position.x,0,right_position.z);
            
            zy = Vector3.Distance(right_position,zero_position);
            zeroY = Vector3.Distance(zero_position,zeroY_Zposition);
            ay = Vector3.Distance(right_position,zeroY_Zposition);

            float Z_rightposition = right_position.z;
            float Y_rightposition = right_position.y;
            float X_rightposition = right_position.x;

            /*Debug.Log(right_position_Y);
            Debug.Log(right_position_Z);*/


            //つかむ動作(サーボモータ4番)
            if (x >= 1)
            {
                t = t + 1;
                if (t <= 135)
                {
                    three_function("'servo_write'", 4, t);
                }
                else{
                    t = 135;
                }
            }
            if (x <= 0.9f)
            {
                t = t - 1;
                if (t >= 45)
                {
                    three_function("'servo_write'", 4, t);
                }
                else
                {
                    t = 45;
                }
            }

            //前と後ろの操作(サーボモータ1番)
            if (Z_rightposition < 0)
            {
                zeroY = Mathf.Abs(zeroY);
                
            }
            else
            {
                zeroY = -Mathf.Abs(zeroY);
                
            }
            float cc = Mathf.Atan2(ay,zeroY);
            float aa = cc * (180f/Mathf.PI);
            w = (int)aa;
            three_function("'servo_write'", 1, w);
            //アームを折り曲げる動作
            
            //横に向く動作(サーボモータ0番)
            
        }

        if (Input.GetKey(KeyCode.W))
        {
            w = w + 1;
            if (w <= 180)
            {
                three_function("'servo_write'", 1, w);
            }
            else
            {
                w = 180;
            }
        }

        if (Input.GetKey(KeyCode.S))
        {
            w = w - 1;
            if (w >= 0)
            {
                three_function("'servo_write'", 1, w);
            }
            else
            {
                w = 0;
            }
        }
        if (Input.GetKey(KeyCode.D))
        {
            q = q + 1;
            if (q <= 180)
            {
                three_function("'servo_write'", 0, q);
            }
            else
            {
                q = 180;
            }
        }
        if (Input.GetKey(KeyCode.A))
        {
            q = q - 1;
            if (q <= 180)
            {
                three_function("'servo_write'", 0, q);
            }
            else
            {
                q = 0;
            }
        }
    }
}