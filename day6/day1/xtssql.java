package day1;

import java.sql.*;
import java.util.Scanner;

public class xtssql {

    // 数据库连接信息
    static final String URL = "jdbc:mysql://localhost:3306/xtsdb";
    static final String USER = "root";
    static final String PASSWORD = "fl3692458121";

    public static void main(String[] args) {
        try (Scanner scanner = new Scanner(System.in)) {
            while (true) {
                System.out.println("\n选择操作：1. 添加  2. 删除  3. 查询  4. 修改  5. 退出");
                int choice = scanner.nextInt();
                scanner.nextLine(); // 清除缓冲区

                switch (choice) {
                    case 1:
                        addTeacher(scanner);
                        break;
                    case 2:
                        deleteTeacher(scanner);
                        break;
                    case 3:
                        queryTeachers();
                        break;
                    case 4:
                        updateTeacher(scanner);
                        break;
                    case 5:
                        System.out.println("退出程序！");
                        return;
                    default:
                        System.out.println("无效的选项，请重新选择！");
                }
            }
        }
    }

    // 添加教师
    private static void addTeacher(Scanner scanner) {
        System.out.println("请输入教师姓名：");
        String tname = scanner.nextLine();
        System.out.println("请输入教师年龄：");
        int age = scanner.nextInt();

        String sql = "INSERT INTO teacher (tname, age) VALUES (?, ?)";
        try (Connection conn = DriverManager.getConnection(URL, USER, PASSWORD);
             PreparedStatement pstmt = conn.prepareStatement(sql)) {

            pstmt.setString(1, tname);
            pstmt.setInt(2, age);
            int rows = pstmt.executeUpdate();
            System.out.println(rows > 0 ? "添加成功！" : "添加失败！");
        } catch (SQLException e) {
            System.out.println("添加失败：" + e.getMessage());
        }
    }

    // 删除教师
    private static void deleteTeacher(Scanner scanner) {
        System.out.println("请输入要删除的教师ID：");
        int teacherid = scanner.nextInt();

        String sql = "DELETE FROM teacher WHERE teacherid = ?";
        try (Connection conn = DriverManager.getConnection(URL, USER, PASSWORD);
             PreparedStatement pstmt = conn.prepareStatement(sql)) {

            pstmt.setInt(1, teacherid);
            int rows = pstmt.executeUpdate();
            System.out.println(rows > 0 ? "删除成功！" : "删除失败！");
        } catch (SQLException e) {
            System.out.println("删除失败：" + e.getMessage());
        }
    }

    // 查询教师
    private static void queryTeachers() {
        String sql = "SELECT * FROM teacher";
        try (Connection conn = DriverManager.getConnection(URL, USER, PASSWORD);
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {

            System.out.printf("%-10s %-20s %-10s%n", "教师ID", "教师名称", "年龄");
            System.out.println("-----------------------------------------");

            while (rs.next()) {
                int teacherid = rs.getInt("teacherid");
                String tname = rs.getString("tname");
                int age = rs.getInt("age");
                System.out.printf("%-10d %-20s %-10d%n", teacherid, tname, age);
            }
        } catch (SQLException e) {
            System.out.println("查询失败：" + e.getMessage());
        }
    }

    // 修改教师信息
    private static void updateTeacher(Scanner scanner) {
        System.out.println("请输入要修改的教师ID：");
        int teacherid = scanner.nextInt();
        scanner.nextLine(); // 清除缓冲区

        System.out.println("请输入新的教师姓名：");
        String tname = scanner.nextLine();

        System.out.println("请输入新的教师年龄：");
        int age = scanner.nextInt();

        String sql = "UPDATE teacher SET tname = ?, age = ? WHERE teacherid = ?";
        try (Connection conn = DriverManager.getConnection(URL, USER, PASSWORD);
             PreparedStatement pstmt = conn.prepareStatement(sql)) {

            pstmt.setString(1, tname);
            pstmt.setInt(2, age);
            pstmt.setInt(3, teacherid);
            int rows = pstmt.executeUpdate();
            System.out.println(rows > 0 ? "修改成功！" : "修改失败！");
        } catch (SQLException e) {
            System.out.println("修改失败：" + e.getMessage());
        }
    }
}
