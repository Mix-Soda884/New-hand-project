using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class CatchLog : MonoBehaviour
{
    public Text logText;  // UIのTextコンポーネントをアタッチする
    private string logContent = "";
    private List<string> logMessages = new List<string>();
    private const int maxCharactersPerLine = 100;  // 表示する1行あたりの最大文字数
    private const int maxLogCount = 50;  // 保持する最大ログ数

    private void OnEnable()
    {
        Application.logMessageReceived += HandleLog;
    }

    private void OnDisable()
    {
        Application.logMessageReceived -= HandleLog;
    }

    private void HandleLog(string logString, string stackTrace, LogType type)
    {
        if (logText == null)
        {
            Debug.LogError("logText is not assigned.");
            return;
        }

        string color;
        switch (type)
        {
            case LogType.Error:
            case LogType.Exception:
                color = "red";
                break;
            case LogType.Warning:
                color = "yellow";
                break;
            default:
                color = "white";
                break;
        }

        // メッセージを1行にカットして長すぎる場合は「...」を追加
        string formattedMessage = $"{type}: {logString}";
        if (formattedMessage.Length > maxCharactersPerLine)
        {
            formattedMessage = formattedMessage.Substring(0, maxCharactersPerLine) + "...";
        }

        formattedMessage = $"<color={color}>{formattedMessage}</color>";

        // ログメッセージをリストに追加
        logMessages.Add(formattedMessage);

        // ログメッセージが最大数を超えた場合、最古のメッセージを削除
        if (logMessages.Count > maxLogCount)
        {
            logMessages.RemoveAt(0);
        }

        // 更新されたログメッセージをテキストに設定
        logText.text = string.Join("\n", logMessages);

    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            Debug.Log("スペースキーが押されました");
        }
    }
}
