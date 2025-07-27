import datetime
import json
import os
from typing import List, Dict, Optional, Tuple


class Transaction:
    """记录每一笔收支交易"""

    def __init__(self, amount: float, category: str, transaction_type: str,
                 date: Optional[datetime.date] = None, description: str = ""):
        """
        初始化交易记录
        :param amount: 金额
        :param category: 分类
        :param transaction_type: 类型，收入(income)或支出(expense)
        :param date: 日期，默认为今天
        :param description: 描述
        """
        self.amount = amount
        self.category = category
        self.type = transaction_type.lower()
        self.date = date if date else datetime.date.today()
        self.description = description

        # 验证交易类型
        if self.type not in ['income', 'expense']:
            raise ValueError("交易类型必须是 'income' 或 'expense'")

    def to_dict(self) -> Dict:
        """将交易转换为字典，用于保存"""
        return {
            'amount': self.amount,
            'category': self.category,
            'type': self.type,
            'date': self.date.isoformat(),
            'description': self.description
        }

    @classmethod
    def from_dict(cls, data: Dict):
        """从字典创建交易对象"""
        return cls(
            amount=data['amount'],
            category=data['category'],
            transaction_type=data['type'],
            date=datetime.date.fromisoformat(data['date']),
            description=data.get('description', '')
        )


class CategoryManager:
    """分类管理"""

    def __init__(self):
        # 初始化默认分类
        self.categories = {
            'income': ['工资', '奖金', '投资收益', '其他收入'],
            'expense': ['餐饮', '交通', '住房', '购物', '娱乐', '医疗', '教育', '其他支出']
        }

    def get_categories(self, transaction_type: str) -> List[str]:
        """获取指定类型的所有分类"""
        return self.categories.get(transaction_type.lower(), [])

    def add_category(self, transaction_type: str, category: str) -> bool:
        """添加新分类"""
        t_type = transaction_type.lower()
        if t_type not in self.categories:
            return False

        if category not in self.categories[t_type]:
            self.categories[t_type].append(category)
            return True
        return False

    def remove_category(self, transaction_type: str, category: str) -> bool:
        """删除分类"""
        t_type = transaction_type.lower()
        if t_type not in self.categories:
            return False

        if category in self.categories[t_type]:
            # 保留至少一个分类
            if len(self.categories[t_type]) > 1:
                self.categories[t_type].remove(category)
                return True
        return False


class AccountingBook:
    """记账本核心类"""

    def __init__(self):
        # 获取脚本所在目录
        script_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_path)
        # 确保数据文件与脚本在同一目录
        self.data_file = os.path.join(script_dir, "accounting_data.json")

        self.transactions: List[Transaction] = []
        self.category_manager = CategoryManager()
        self.load_data()

    def add_transaction(self, transaction: Transaction) -> None:
        """添加交易记录"""
        self.transactions.append(transaction)
        self.save_data()

    def get_transactions(self, start_date: Optional[datetime.date] = None,
                         end_date: Optional[datetime.date] = None,
                         transaction_type: Optional[str] = None,
                         category: Optional[str] = None) -> List[Transaction]:
        """筛选交易记录"""
        filtered = []

        for t in self.transactions:
            # 日期筛选
            if start_date and t.date < start_date:
                continue
            if end_date and t.date > end_date:
                continue

            # 类型筛选
            if transaction_type and t.type != transaction_type.lower():
                continue

            # 分类筛选
            if category and t.category != category:
                continue

            filtered.append(t)

        return filtered

    def get_balance(self) -> float:
        """计算当前余额"""
        income = sum(t.amount for t in self.transactions if t.type == 'income')
        expense = sum(
            t.amount for t in self.transactions if t.type == 'expense')
        return income - expense

    def get_summary_by_period(self, start_date: datetime.date,
                              end_date: datetime.date) -> Tuple[float, float, float]:
        """获取指定时间段的收支汇总"""
        transactions = self.get_transactions(start_date, end_date)
        income = sum(t.amount for t in transactions if t.type == 'income')
        expense = sum(t.amount for t in transactions if t.type == 'expense')
        return income, expense, income - expense

    def get_category_summary(self, transaction_type: str,
                             start_date: Optional[datetime.date] = None,
                             end_date: Optional[datetime.date] = None) -> Dict[str, float]:
        """按分类汇总收支"""
        transactions = self.get_transactions(
            start_date, end_date, transaction_type)

        summary = {}
        for t in transactions:
            if t.category in summary:
                summary[t.category] += t.amount
            else:
                summary[t.category] = t.amount

        return summary

    def save_data(self) -> None:
        """保存数据到文件"""
        data = {
            'transactions': [t.to_dict() for t in self.transactions],
            'categories': self.category_manager.categories
        }
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存数据出错: {e}")
            raise  # 让异常直接显示出来

    def load_data(self) -> None:
        """从文件加载数据"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

                # 加载交易记录
                self.transactions = [Transaction.from_dict(
                    t) for t in data.get('transactions', [])]

                # 加载分类
                if 'categories' in data:
                    self.category_manager.categories = data['categories']

        except FileNotFoundError:
            # 如果文件不存在，使用默认数据
            pass
        except Exception as e:
            print(f"加载数据出错: {e}")

    def print_data_file_path(self):
        """打印数据文件保存路径"""
        print(f"数据文件保存路径：{self.data_file}")


def main():
    """简单的命令行界面演示"""
    book = AccountingBook()
    print("欢迎使用个人记账软件！")

    # 打印数据文件路径
    book.print_data_file_path()

    while True:
        print("\n请选择操作:")
        print("1. 记录收入")
        print("2. 记录支出")
        print("3. 查看交易记录")
        print("4. 查看收支汇总")
        print("5. 查看分类统计")
        print("6. 管理分类")
        print("0. 退出")

        choice = input("请输入操作编号: ")

        if choice == '0':
            print("谢谢使用，再见！")
            break

        elif choice == '1':  # 记录收入
            print("\n记录收入")
            categories = book.category_manager.get_categories('income')
            print(f"收入分类: {', '.join(categories)}")

            try:
                amount = float(input("请输入金额: "))
                category = input("请输入分类: ")
                description = input("请输入描述 (可选): ")

                if category not in categories:
                    print(f"分类不存在，已自动添加新分类: {category}")
                    book.category_manager.add_category('income', category)

                transaction = Transaction(
                    amount, category, 'income', description=description)
                book.add_transaction(transaction)
                print("记录成功！")
            except ValueError as e:
                print(f"输入错误: {e}")

        elif choice == '2':  # 记录支出
            print("\n记录支出")
            categories = book.category_manager.get_categories('expense')
            print(f"支出分类: {', '.join(categories)}")

            try:
                amount = float(input("请输入金额: "))
                category = input("请输入分类: ")
                description = input("请输入描述 (可选): ")

                if category not in categories:
                    print(f"分类不存在，已自动添加新分类: {category}")
                    book.category_manager.add_category('expense', category)

                transaction = Transaction(
                    amount, category, 'expense', description=description)
                book.add_transaction(transaction)
                print("记录成功！")
            except ValueError as e:
                print(f"输入错误: {e}")

        elif choice == '3':  # 查看交易记录
            print("\n查看交易记录")
            transactions = book.get_transactions()

            if not transactions:
                print("没有交易记录")
                continue

            print(f"{'日期':<12} {'类型':<6} {'分类':<6} {'金额':<8} 描述")
            print("-" * 50)
            for t in sorted(transactions, key=lambda x: x.date, reverse=True):
                print(
                    f"{t.date.isoformat():<12} {t.type:<6} {t.category:<6} {t.amount:<8} {t.description}")

        elif choice == '4':  # 查看收支汇总
            print("\n查看收支汇总")
            today = datetime.date.today()
            first_day = today.replace(day=1)

            income, expense, balance = book.get_summary_by_period(
                first_day, today)
            print(f"本月收入: {income:.2f}")
            print(f"本月支出: {expense:.2f}")
            print(f"本月结余: {balance:.2f}")
            print(f"当前总余额: {book.get_balance():.2f}")

        elif choice == '5':  # 查看分类统计
            print("\n查看分类统计")
            print("1. 收入分类统计")
            print("2. 支出分类统计")
            sub_choice = input("请选择: ")

            if sub_choice == '1':
                summary = book.get_category_summary('income')
                print("\n收入分类统计:")
            elif sub_choice == '2':
                summary = book.get_category_summary('expense')
                print("\n支出分类统计:")
            else:
                print("无效选择")
                continue

            if not summary:
                print("没有相关记录")
                continue

            total = sum(summary.values())
            for category, amount in summary.items():
                percentage = (amount / total) * 100 if total > 0 else 0
                print(f"{category}: {amount:.2f} ({percentage:.1f}%)")

        elif choice == '6':  # 管理分类
            print("\n管理分类")
            print("1. 查看收入分类")
            print("2. 查看支出分类")
            print("3. 添加分类")
            print("4. 删除分类")
            sub_choice = input("请选择: ")

            if sub_choice == '1':
                print("收入分类:", book.category_manager.get_categories('income'))
            elif sub_choice == '2':
                print("支出分类:", book.category_manager.get_categories('expense'))
            elif sub_choice == '3':
                t_type = input("请输入类型 (income/expense): ")
                category = input("请输入新分类名称: ")
                if book.category_manager.add_category(t_type, category):
                    print(f"分类 '{category}' 添加成功")
                    book.save_data()
                else:
                    print("分类添加失败")
            elif sub_choice == '4':
                t_type = input("请输入类型 (income/expense): ")
                category = input("请输入要删除的分类名称: ")
                if book.category_manager.remove_category(t_type, category):
                    print(f"分类 '{category}' 删除成功")
                    book.save_data()
                else:
                    print("分类删除失败")
            else:
                print("无效选择")

        else:
            print("无效的操作，请重新选择")


if __name__ == "__main__":
    main()
