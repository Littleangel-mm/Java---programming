// package xcx;

// import java.util.Random;

// public class ClassLottery {
//     public static void main(String[] args) {
//         // 班级成员名单
//         String[] classNames = {
//             "张三", "李四", "王五", "赵六", "钱七", "孙八", "周九", "吴十", 
//             "郑十一", "冯十二", "陈十三", "褚十四", "卫十五", "蒋十六", "沈十七"
//         };

//         // 使用 Random 类生成随机数
//         Random random = new Random();

//         // 随机选择一个班级成员的名字
//         int index = random.nextInt(classNames.length);

//         // 显示结果
//         System.out.println("抽中的同学是: " + classNames[index]);
//     }
// }



package Day1;
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.Random;

public class ClassLottery {
    // 班级成员名单
    private static final String[] classNames = {
        "张三", "李四", "王五", "赵六", "钱七", "孙八", "周九", "吴十", 
        "郑十一", "冯十二", "陈十三", "褚十四", "卫十五", "蒋十六", "沈十七"
    };

    // 随机数生成器
    private static Random random = new Random();

    public static void main(String[] args) {
        // 创建主窗口
        JFrame frame = new JFrame("班级抽奖系统");

        // 设置窗口大小与关闭操作
        frame.setSize(400, 300);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // 创建面板
        JPanel panel = new JPanel();
        panel.setLayout(new BorderLayout());

        // 设置标签显示区域
        JLabel resultLabel = new JLabel("请点击下面的按钮抽取同学...", JLabel.CENTER);
        resultLabel.setFont(new Font("微软雅黑", Font.PLAIN, 20)); // 设置字体和大小
        resultLabel.setForeground(Color.BLUE); // 设置文字颜色
        panel.add(resultLabel, BorderLayout.CENTER);

        // 创建抽奖按钮
        JButton drawButton = new JButton("抽取同学");
        drawButton.setFont(new Font("微软雅黑", Font.PLAIN, 20));
        drawButton.setBackground(Color.CYAN); // 设置按钮背景色
        drawButton.setForeground(Color.BLACK); // 设置按钮文字颜色
        panel.add(drawButton, BorderLayout.SOUTH);

        // 抽奖按钮点击事件
        drawButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                // 随机抽取一个班级成员
                int index = random.nextInt(classNames.length);
                String selectedName = classNames[index];
                // 更新标签显示抽取的结果
                resultLabel.setText("抽中的同学是: " + selectedName);
            }
        });

        // 将面板添加到窗口
        frame.add(panel);

        // 设置窗口可见
        frame.setVisible(true);
    }
}

