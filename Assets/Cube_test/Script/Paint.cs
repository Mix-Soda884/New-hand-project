
using System.Collections.Generic;
using UnityEngine;
using Leap;
using Leap.Unity;


public class Paint : MonoBehaviour
{
    [SerializeField] GameObject LineObjectPrefab;
    Transform myTrans;
    Vector3 tipPos;

    private GameObject CurrentLineObject = null;

    private void Update()
    {
        myTrans = this.transform;
        tipPos = myTrans.position;

        //スペースキーを押した瞬間
        if (Input.GetKeyDown(KeyCode.Space)) CurrentLineObject = Instantiate(LineObjectPrefab, new Vector3(0, 0, 0), Quaternion.identity);


        //スペースキーを押してる間
        if (Input.GetKey(KeyCode.Space))
        {

            //ゲームオブジェクトからLineRendererコンポーネントを取得
            LineRenderer render = CurrentLineObject.GetComponent<LineRenderer>();

            //LineRendererからPositionsのサイズを取得
            int NextPositionIndex = render.positionCount;

            //LineRendererのPositionsのサイズを増やす
            render.positionCount = NextPositionIndex + 1;

            //LineRendererのPositionsに現在の指先の位置情報を追加
            render.SetPosition(NextPositionIndex, tipPos);
            Debug.Log(tipPos.x);
        }

        //スペースキーを押してないとき
        else //スペースキーから指を離したとき
        {
            if (CurrentLineObject != null)
            {
                //現在描画中の線があったらnullにして次の線を描けるようにする。
                CurrentLineObject = null;
            }
        }


    }

}
