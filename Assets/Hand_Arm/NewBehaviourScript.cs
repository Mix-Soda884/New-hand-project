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
    public LeapServiceProvider m_Provider;
    GameObject m_ProviderObject;
    public SerialHandler serialHandler;
    Vector3 right_normal;
    Vector3 left_normal;
    Vector3 right_direction;
    Vector3 left_direction;
    Vector3 right_position;
    Vector3 left_position;
    private Transform emptyObjectTransform;
    Vector3 r1;
    Vector3 r0;
    float rx;
    float lx;
    float ay;
    float zy;
    float zeroY;
    int q = 90;
    int w = 90;
    int e = 180;
    int r = 100;
    int t = 180;

    int s0;
    int s1;
    int s2;

    int s4openHand; // ひらき角

    public VisibleBallHand handScript;
    public Visiblehand Visiblehand;

    private bool isSending = false;  // 送信中かどうかのフラグ
    private float sendTimeout = 0.02f;  // 送信のタイムアウト時間（秒）
    private float sendFrequency = 0.5f;  // 送信の頻度（秒）

    IEnumerator SendDataWithTimeout(string data)
    {
        isSending = true;
        serialHandler.Write(data);

        float timer = 0;

        // タイムアウトまで待機
        while (timer < sendTimeout)
        {
            yield return null;  // 1フレーム待機
            timer += Time.deltaTime;

            // レスポンスがあれば送信成功として処理
            if (serialHandler.isDataAvailable)
            {
                Debug.Log("Data sent successfully");
                isSending = false;
                yield break;
            }
        }

        // タイムアウトした場合は中断
        //Debug.LogWarning("Data send timeout. Aborting send.");
        isSending = false;
    }
    IEnumerator SendDataWithFrequency()
    {
        while (true)
        {
            // 送信処理
            string p1 = "{'start':[value1, value2, value3]}\n";  // 適切な値に置き換える
            byte[] p1EncodedBytes = Encoding.GetEncoding("gbk").GetBytes(p1);
            string p1EncodedString = Encoding.GetEncoding("gbk").GetString(p1EncodedBytes);

            if (!isSending)
            {
                StartCoroutine(SendDataWithTimeout(p1EncodedString));
            }

            yield return new WaitForSeconds(sendFrequency);
        }
    }

    void three_function(string a, int b, int c)
    {
        string p1;
        p1 = "{'start':" + $"[{a},{b},{c}]" + "}\n";
//        print(p1);
        byte[] p1EncodedBytes = Encoding.GetEncoding("gbk").GetBytes(p1);
        string p1EncodedString = Encoding.GetEncoding("gbk").GetString(p1EncodedBytes);
        serialHandler.Write(p1EncodedString);
        //Debug.Log(p1EncodedString);
        //ser.write("{'start':['pinmode',13,0]}\n".encode("gbk"))

        if (!isSending)
        {
            StartCoroutine(SendDataWithTimeout(p1EncodedString));
        }
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

        s0 = q;
        s1 = w;
        s2 = e;
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
        Hand leftHand = null;

        foreach (Hand hand in frame.Hands)
        {
            if (hand.IsRight)
            {
                rightHand = hand; // 右手情報を代入
                break; // 右手が見つかったらループを抜ける
            }
            if (hand.IsLeft)
            {
                leftHand = hand; // 左手情報を代入
                break; // 左手が見つかったらループを抜ける
            }
        }

        if (rightHand != null)
        {
            r0 = rightHand.Fingers[0].TipPosition;
            r1 = rightHand.Fingers[1].TipPosition;
            rx = Vector3.Distance(r1, r0);
            //Debug.Log("FingerDist " + rx.ToString());

            right_normal = rightHand.PalmNormal;
            right_direction = rightHand.Direction;
            right_position = rightHand.PalmPosition;

            emptyObjectTransform = GameObject.Find("Leap motion Controller").transform;
            Vector3 zero_position = new Vector3(0,0.3f,0);
            Vector3 zeroY_Zposition = new Vector3(right_position.x,0,right_position.z);
            
            zeroY = Vector3.Distance(zero_position,zeroY_Zposition);
            ay = Vector3.Distance(right_position,zeroY_Zposition);
            float re = Vector3.Distance(right_position,zero_position); 

            Vector3 direction = right_position-zero_position;

            //つかむ動作(サーボモータ4番)
            if (rx >= 0.1f || Input.GetKey(KeyCode.O))
            {
                /*
                t = t + 10;
                if (t <= 180)
                {
                    three_function("'servo_write'", 4, t);
                }
                else{
                    t = 180;
                }
                */
                //three_function("'servo_write'", 4, 180);
                s4openHand = 120;
            }
            else if (rx <= 0.05f || Input.GetKey(KeyCode.C))
            {
                /*
                                t = t - 10;
                                if (t >= 40)
                                {
                                    three_function("'servo_write'", 4, t);
                                }
                                else
                                {
                                    t = 40;
                                }
                */
                //three_function("'servo_write'", 4, 40);
                s4openHand = 75;
            }

            //横の動作(サーボモータ0番)
            float xp = Mathf.Rad2Deg * Mathf.Atan2(direction.z,direction.x);
            q = (int)xp;
            if (q < 0) q = q * -1;
            if (q > 180) q = 180;
            s0 = (int)(s0 * 0.9f+q*0.1f);
            if (s0 < 0) s0 = 0;
            if (s0 > 180) s0 = 180;
            //three_function("'servo_write'", 0, s0);
            
            //前と後ろの操作(サーボモータ1番)
            //Debug.Log(direction);
            float cc = Mathf.Rad2Deg * Mathf.Atan2(direction.z,direction.y-0.1f);    
            w = (int)cc;
            
            if (w < 0) w = 0;
            if (w > 120) w = 120;
            

            //アームを折り曲げる動作(サーボモータ2番)
            float hy = re /3 ;

            float arm = 0.07f;
            float secondarm = 0;
            if (hy < arm){
                secondarm = Mathf.Rad2Deg * Mathf.Acos(hy/arm);
            }

            secondarm = secondarm * 1.1f;
            e = (int)secondarm;

            
            int ren = (int)re;

            if (re <= 0.25) q = -q * (ren * 4 - 1);

            s0 = (int)(s0 * 0.9f + q * 0.1f);
            if (s0 < 0) s0 = 0;
            if (s0 > 180) s0 = 180;

            if (e < 0) e = 0;
            if (e > 150) e = 150;

            if (re <= 0.25) w = -w * (ren * 4 - 1);
            if (re <= 0.25) e = -e * (ren * 4 - 1);

            s1 = (int)(s1 * 0.9f +(90 - e + w)*0.1f);
            if (s1 < 0) s1 = 0;
            if (s1 > 180) s1 = 180;

            if (e < 0) e = 0;
            if (e > 135) e = 135;
            s2 = (int)(s2 * 0.9f + (180 - e * 2)*0.1f);
            if (s2 < 0) s2 = 0;
            if (s2 > 180) s2 = 180;


            three_function("'servo_write'", 4, s4openHand);
            three_function("'servo_write'", 0, s0);
            three_function("'servo_write'", 1, s1);
            three_function("'servo_write'", 2, s2);
        }



        if (leftHand != null)
        {
            r0 = leftHand.Fingers[0].TipPosition;
            r1 = leftHand.Fingers[1].TipPosition;
            lx = Vector3.Distance(r1, r0);
            Debug.Log("FingerDist " + lx.ToString());

            left_normal = leftHand.PalmNormal;
            left_direction = leftHand.Direction;
            left_position = leftHand.PalmPosition;

            emptyObjectTransform = GameObject.Find("Leap motion Controller").transform;
            Vector3 zero_position = new Vector3(0, 0.3f, 0);
            Vector3 zeroY_Zposition = new Vector3(left_position.x, 0, left_position.z);

            zeroY = Vector3.Distance(zero_position, zeroY_Zposition);
            ay = Vector3.Distance(left_position, zeroY_Zposition);
            float re = Vector3.Distance(left_position, zero_position);

            Vector3 direction = left_position - zero_position;

            //つかむ動作(サーボモータ4番)
            if (lx >= 0.1f || Input.GetKey(KeyCode.O))
            {
                /*
                t = t + 10;
                if (t <= 180)
                {
                    three_function("'servo_write'", 4, t);
                }
                else{
                    t = 180;
                }
                */
                //                three_function("'servo_write'", 4, 180);
                s4openHand = 120;
            }
            else if (lx <= 0.05f || Input.GetKey(KeyCode.C))
            {
                /*
                                t = t - 10;
                                if (t >= 40)
                                {
                                    three_function("'servo_write'", 4, t);
                                }
                                else
                                {
                                    t = 40;
                                }
                */
                //                three_function("'servo_write'", 4, 40);
                s4openHand = 75;
            }

            //横の動作(サーボモータ0番)
            float xp = Mathf.Rad2Deg * Mathf.Atan2(direction.z, direction.x);
            q = (int)xp;
            if (q < 0) q = q * -1;
            if (q > 180) q = 180;
            s0 = (int)(s0 * 0.9f + q * 0.1f);
            if (s0 < 0) s0 = 0;
            if (s0 > 180) s0 = 180;
            //            three_function("'servo_write'", 0, s0);

            //前と後ろの操作(サーボモータ1番)
            //Debug.Log(direction);
            float cc = Mathf.Rad2Deg * Mathf.Atan2(direction.z, direction.y - 0.1f);
            //cc = cc * 1.2f;       
            w = (int)cc;
            if (w < 0) w = 0;
            if (w > 130) w = 130;


            //アームを折り曲げる動作(サーボモータ2番)
            float hy = re / 3;

            float arm = 0.07f;
            float secondarm = 0;
            if (hy < arm)
            {
                secondarm = Mathf.Rad2Deg * Mathf.Acos(hy / arm);
            }

            secondarm = secondarm * 1.1f;
            e = (int)secondarm;
            if (e < 0) e = 0;
            if (e > 150) e = 150;

            s1 = (int)(s1 * 0.9f + (90 - e + w) * 0.1f);
            if (s1 < 0) s1 = 0;
            if (s1 > 180) s1 = 180;

            if (e < 0) e = 0;
            if (e > 135) e = 135;
            s2 = (int)(s2 * 0.9f + (180 - e * 2) * 0.1f);
            if (s2 < 0) s2 = 0;
            if (s2 > 180) s2 = 180;


            three_function("'servo_write'", 4, s4openHand);
            three_function("'servo_write'", 0, s0);
            three_function("'servo_write'", 1, s1);
            three_function("'servo_write'", 2, s2);
        }
    }
}
